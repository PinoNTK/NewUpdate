import re
import tensorflow as tf
from . import utils_nlp,utils_tf

from sklearn.metrics.classification import classification_report
from sklearn.metrics import confusion_matrix
import codecs


def BLSTM(input, hidden_state_dimension, initializer, sequence_length=None, output_sequence=True):
    with tf.variable_scope("bidirectional_LSTM"):
        if sequence_length == None:
            batch_size = 1
            sequence_length = tf.shape(input)[1]
            sequence_length = tf.expand_dims(sequence_length, axis=0, name='sequence_length')
        else:
            batch_size = tf.shape(sequence_length)[0]

        lstm_cell = {}
        initial_state = {}
        for direction in ["forward", "backward"]:
            with tf.variable_scope(direction):
                # LSTM cell
                lstm_cell[direction] = tf.contrib.rnn.CoupledInputForgetGateLSTMCell(hidden_state_dimension,
                                                                                     forget_bias=1.0,
                                                                                     initializer=initializer,
                                                                                     state_is_tuple=True)
                # initial state: http://stackoverflow.com/questions/38441589/tensorflow-rnn-initial-state
                initial_cell_state = tf.get_variable("initial_cell_state", shape=[1, hidden_state_dimension],
                                                     dtype=tf.float32, initializer=initializer)
                initial_output_state = tf.get_variable("initial_output_state", shape=[1, hidden_state_dimension],
                                                       dtype=tf.float32, initializer=initializer)
                c_states = tf.tile(initial_cell_state, tf.stack([batch_size, 1]))
                h_states = tf.tile(initial_output_state, tf.stack([batch_size, 1]))
                initial_state[direction] = tf.contrib.rnn.LSTMStateTuple(c_states, h_states)

        # sequence_length must be provided for tf.nn.bidirectional_dynamic_rnn due to internal bug
        outputs, final_states = tf.nn.bidirectional_dynamic_rnn(lstm_cell["forward"],
                                                                lstm_cell["backward"],
                                                                input,
                                                                dtype=tf.float32,
                                                                sequence_length=sequence_length,
                                                                initial_state_fw=initial_state["forward"],
                                                                initial_state_bw=initial_state["backward"])
        if output_sequence == True:
            outputs_forward, outputs_backward = outputs
            output = tf.concat([outputs_forward, outputs_backward], axis=2, name='output_sequence')
        else:
            # max pooling
            #             outputs_forward, outputs_backward = outputs
            #             output = tf.concat([outputs_forward, outputs_backward], axis=2, name='output_sequence')
            #             output = tf.reduce_max(output, axis=1, name='output')
            # last pooling
            final_states_forward, final_states_backward = final_states
            output = tf.concat([final_states_forward[1], final_states_backward[1]], axis=1, name='output')

    return output


use_lstm_character = False

class BLSTM_CRF(object):
    """
    An LSTM architecture for named entity recognition.
    Uses a character embedding layer followed by an LSTM to generate vector representation from characters for each token.
    Then the character vector is concatenated with token embedding vector, which is input to another LSTM  followed by a CRF layer.
    """

    def __init__(self, dataset, token_embedding_dimension, character_lstm_hidden_state_dimension,
                 token_lstm_hidden_state_dimension, character_embedding_dimension,vector_extend_dimension = None,
                 freeze_token_embeddings=False,
                 learning_rate=0.005, gradient_clipping_value=5.0, optimizer='sgd', maximum_number_of_epochs=30,name = 'ner'):
        tf.reset_default_graph()
        self.sess = tf.Session()

        self.verbose = True
        self.input_token_indices = tf.placeholder(tf.int32, [None], name="input_token_indices")
        # self.input_label_indices_vector = tf.placeholder(tf.float32, [None, dataset.number_of_classes],name="input_label_indices_vector")
        self.input_label_indices_flat = tf.placeholder(tf.int32, [None], name="input_label_indices_flat")
        self.input_token_character_indices = tf.placeholder(tf.int32, [None, None], name="input_token_indices")
        self.input_token_lengths = tf.placeholder(tf.int32, [None], name="input_token_lengths")
        self.dropout_keep_prob = tf.placeholder(tf.float32, name="dropout_keep_prob")
        if vector_extend_dimension == None:
            vector_extend_dimension = dataset.size_pattern_vector
        self.input_token_patterns = tf.placeholder(tf.float32,[None,vector_extend_dimension],name="input_token_pattern")
        # Internal parameters
        initializer = tf.contrib.layers.xavier_initializer()

        # Token embedding layer
        with tf.variable_scope("token_embedding"):
            self.token_embedding_weights = tf.get_variable(
                "token_embedding_weights",
                shape=[len(dataset.tokens), token_embedding_dimension],
                initializer=initializer,
                trainable=not freeze_token_embeddings)
            embedded_tokens = tf.nn.embedding_lookup(self.token_embedding_weights, self.input_token_indices)

        # Character-level LSTM
        # Idea: reshape so that we have a tensor [number_of_token, max_token_length, token_embeddings_size], which we pass to the LSTM

        if use_lstm_character:
            # Character embedding layer
            with tf.variable_scope("character_embedding"):
                self.character_embedding_weights = tf.get_variable("character_embedding_weights",
                                                                   shape=[dataset.alphabet_size,
                                                                          character_embedding_dimension],
                                                                   initializer=initializer)
                embedded_characters = tf.nn.embedding_lookup(self.character_embedding_weights,
                                                             self.input_token_character_indices,
                                                             name='embedded_characters')
                if self.verbose: print("embedded_characters: {0}".format(embedded_characters))
            # utils_tf.variable_summaries(self.character_embedding_weights)

            # Character LSTM layer
            with tf.variable_scope('character_lstm') as vs:
                character_lstm_output = BLSTM(embedded_characters,
                                              character_lstm_hidden_state_dimension,
                                              initializer,
                                              sequence_length=self.input_token_lengths,
                                              output_sequence=False)
                self.character_lstm_variables = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=vs.name)



        # utils_tf.variable_summaries(self.token_embedding_weights)

            # Concatenate character LSTM outputs and token embeddings
            with tf.variable_scope("concatenate_token_and_character_vectors"):
                token_lstm_input = tf.concat([character_lstm_output,tf.concat( [embedded_tokens,self.input_token_patterns],1)], axis=1, name='token_lstm_input')
                if self.verbose:
                    print('embedded_tokens: {0}'.format(embedded_tokens))
                    print("token_lstm_input: {0}".format(token_lstm_input))

        else:
            with tf.variable_scope("concatenate_token_and_character_vectors"):
                token_lstm_input = tf.concat([embedded_tokens, self.input_token_patterns], axis=1,name='token_lstm_input')
                if self.verbose:
                    print('embedded_tokens: {0}'.format(embedded_tokens))
                    print("token_lstm_input: {0}".format(token_lstm_input))

        # Add dropout
        with tf.variable_scope("dropout"):
            token_lstm_input_drop = tf.nn.dropout(token_lstm_input, self.dropout_keep_prob,
                                                  name='token_lstm_input_drop')
            if self.verbose: print("token_lstm_input_drop: {0}".format(token_lstm_input_drop))
            # https://www.tensorflow.org/api_guides/python/contrib.rnn
            # Prepare data shape to match `rnn` function requirements
            # Current data input shape: (batch_size, n_steps, n_input)
            # Required shape: 'n_steps' tensors list of shape (batch_size, n_input)
            token_lstm_input_drop_expanded = tf.expand_dims(token_lstm_input_drop, axis=0,
                                                            name='token_lstm_input_drop_expanded')
            if self.verbose: print("token_lstm_input_drop_expanded: {0}".format(token_lstm_input_drop_expanded))

        # Token LSTM layer
        with tf.variable_scope('token_lstm') as vs:
            token_lstm_output = BLSTM(token_lstm_input_drop_expanded,
                                      token_lstm_hidden_state_dimension, initializer,
                                      output_sequence=True)
            token_lstm_output_squeezed = tf.squeeze(token_lstm_output, axis=0)
            self.token_lstm_variables = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=vs.name)

        # Needed only if Bidirectional LSTM is used for token level
        with tf.variable_scope("feedforward_after_lstm") as vs:
            W = tf.get_variable(
                "W",
                shape=[2 * token_lstm_hidden_state_dimension, token_lstm_hidden_state_dimension],
                initializer=initializer)
            b = tf.Variable(tf.constant(0.0, shape=[token_lstm_hidden_state_dimension]), name="bias")
            outputs = tf.nn.xw_plus_b(token_lstm_output_squeezed, W, b, name="output_before_tanh")
            outputs = tf.nn.tanh(outputs, name="output_after_tanh")
            #             utils_tf.variable_summaries(W)
            #             utils_tf.variable_summaries(b)
            self.token_lstm_variables += tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=vs.name)

        with tf.variable_scope("feedforward_before_crf") as vs:
            W = tf.get_variable(
                "W",
                shape=[token_lstm_hidden_state_dimension, dataset.number_of_classes],
                initializer=initializer)
            b = tf.Variable(tf.constant(0.0, shape=[dataset.number_of_classes]), name="bias")
            scores = tf.nn.xw_plus_b(outputs, W, b, name="scores")
            self.unary_scores = scores

            #             utils_tf.variable_summaries(W)
            #             utils_tf.variable_summaries(b)
            self.feedforward_variables = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=vs.name)

        # CRF layer
        with tf.variable_scope("crf") as vs:
            # Add start and end tokens
            small_score = -1000.0
            large_score = 0.0
            sequence_length = tf.shape(self.unary_scores)[0]
            unary_scores_with_start_and_end = tf.concat(
                [self.unary_scores, tf.tile(tf.constant(small_score, shape=[1, 2]), [sequence_length, 1])], 1)
            start_unary_scores = [[small_score] * dataset.number_of_classes + [large_score, small_score]]
            end_unary_scores = [[small_score] * dataset.number_of_classes + [small_score, large_score]]
            self.unary_scores = tf.concat([start_unary_scores, unary_scores_with_start_and_end, end_unary_scores], 0)
            start_index = dataset.number_of_classes
            end_index = dataset.number_of_classes + 1
            input_label_indices_flat_with_start_and_end = tf.concat(
                [tf.constant(start_index, shape=[1]), self.input_label_indices_flat,
                 tf.constant(end_index, shape=[1])], 0)

            # Apply CRF layer
            sequence_length = tf.shape(self.unary_scores)[0]
            sequence_lengths = tf.expand_dims(sequence_length, axis=0, name='sequence_lengths')
            unary_scores_expanded = tf.expand_dims(self.unary_scores, axis=0, name='unary_scores_expanded')
            input_label_indices_flat_batch = tf.expand_dims(input_label_indices_flat_with_start_and_end, axis=0,
                                                            name='input_label_indices_flat_batch')
            if self.verbose: print('unary_scores_expanded: {0}'.format(unary_scores_expanded))
            if self.verbose: print('input_label_indices_flat_batch: {0}'.format(input_label_indices_flat_batch))
            if self.verbose: print("sequence_lengths: {0}".format(sequence_lengths))
            # https://github.com/tensorflow/tensorflow/tree/master/tensorflow/contrib/crf
            # Compute the log-likelihood of the gold sequences and keep the transition params for inference at test time.
            self.transition_parameters = tf.get_variable(
                "transitions",
                shape=[dataset.number_of_classes + 2, dataset.number_of_classes + 2],
                initializer=initializer)
            #                 utils_tf.variable_summaries(self.transition_parameters)
            log_likelihood, _ = tf.contrib.crf.crf_log_likelihood(
                unary_scores_expanded, input_label_indices_flat_batch, sequence_lengths,
                transition_params=self.transition_parameters)
            self.loss = tf.reduce_mean(-log_likelihood, name='cross_entropy_mean_loss')
            # self.accuracy = tf.constant(1)

            self.crf_variables = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=vs.name)

        # self.predictions,_ = tf.contrib.crf.viterbi_decode(self.unary_scores,self.transition_parameters)
        # tf.add_to_collection(name="predictions",value=self.predictions)
        # self.predict = tf.contrib.crf.viterbi_decode(self.unary_scores,self.transition_parameters)
        self.define_training_procedure(learning_rate=learning_rate, gradient_clipping_value=gradient_clipping_value,
                                       optimizer=optimizer)
        self.summary_op = tf.summary.merge_all()
        self.saver = tf.train.Saver(max_to_keep=maximum_number_of_epochs)  # defaults to saving all variables

        self.sess.run(tf.global_variables_initializer())

    def define_training_procedure(self, learning_rate, gradient_clipping_value, optimizer='sgd'):
        # Define training procedure
        self.global_step = tf.Variable(0, name="global_step", trainable=False)
        if optimizer == 'adam':
            self.optimizer = tf.train.AdamOptimizer(learning_rate)
        elif optimizer == 'sgd':
            self.optimizer = tf.train.GradientDescentOptimizer(learning_rate)
        elif optimizer == 'adadelta':
            self.optimizer = tf.train.AdadeltaOptimizer(learning_rate)
        else:
            raise ValueError('The lr_method parameter must be either adadelta, adam or sgd.')

        grads_and_vars = self.optimizer.compute_gradients(self.loss)
        if gradient_clipping_value:
            grads_and_vars = [(tf.clip_by_value(grad, -gradient_clipping_value,
                                                gradient_clipping_value), var)
                              for grad, var in grads_and_vars]
        # By defining a global_step variable and passing it to the optimizer we allow TensorFlow handle the counting of training steps for us.
        # The global step will be automatically incremented by one every time you execute train_op.
        self.train_op = self.optimizer.apply_gradients(grads_and_vars, global_step=self.global_step)

    def train_step(self,token_indices, character_indices_padded, token_lengths, pattern ,label_indices , dropout_rate = 0.5 ):
        for sequence_number in range(len(token_indices)):
            feed_dict = {
                self.input_token_indices: token_indices[sequence_number],
                self.input_token_character_indices: character_indices_padded[sequence_number],
                self.input_token_lengths: token_lengths[sequence_number],
                self.input_token_patterns: pattern[sequence_number],

                self.input_label_indices_flat: label_indices[sequence_number],
                # self.input_label_indices_vector: label_vector[sequence_number],
                self.dropout_keep_prob: 1 - dropout_rate,

            }
            _, loss, transition_params_trained =self.sess.run([self.train_op,  self.loss,  self.transition_parameters],feed_dict)
            # if sequence_number % 2000 ==0:
            #     print('loss : ',loss)
        return transition_params_trained

    def predict_step(self,token_indices,character_indices_padded,token_lengths,pattern):
        feed_dict = {
            self.input_token_indices: token_indices,
            self.input_token_character_indices: character_indices_padded,
            self.input_token_lengths: token_lengths,
            self.input_token_patterns: pattern,
            self.dropout_keep_prob: 1.,
        }
        unary_scores, transition_params_trained = self.sess.run([self.unary_scores, self.transition_parameters], feed_dict)
        #
        predictions, _ = tf.contrib.crf.viterbi_decode(unary_scores, transition_params_trained)
        # tensor_pre,_ = tf.contrib.crf.viterbi_decode(self.unary_scores,self.transition_parameters)

        # predictions = sess.run(self.predictions,feed_dict)

        predictions = predictions[1:-1]

        assert (len(predictions) == len(token_indices))

        return predictions
    def predict(self,token_indices, character_indices_padded, token_lengths, pattern ):
        all_predictions = []
        all_y_true = []
        # output_filepath = os.path.join(stats_graph_folder, '{1:03d}_{0}.txt'.format(dataset_type,epoch_number))
        # output_file = codecs.open(output_filepath, 'w', 'UTF-8')
        # original_conll_file = codecs.open(dataset_filepaths[dataset_type], 'r', 'UTF-8')

        for i in range(len(token_indices)):
            feed_dict = {
                self.input_token_indices: token_indices[i],
                self.input_token_character_indices: character_indices_padded[i],
                self.input_token_lengths: token_lengths[i],
                self.input_token_patterns: pattern[i],
                self.dropout_keep_prob: 1.,
            }
            unary_scores, transition_params_trained = self.sess.run([self.unary_scores, self.transition_parameters], feed_dict)


            predictions, _ = tf.contrib.crf.viterbi_decode(unary_scores, transition_params_trained)
            # predictions = sess.run(self.predictions,feed_dict)
            predictions = predictions[1:-1]

            assert (len(predictions) == len(token_indices[i]))

            all_predictions.append(predictions)
        return all_predictions

    def evaluate(self,vocab,token_indices, character_indices_padded, token_lengths, pattern ,label_indices,datatype='train'):
        all_predictions = []
        all_y_true = []
        # output_filepath = os.path.join(stats_graph_folder, '{1:03d}_{0}.txt'.format(dataset_type,epoch_number))
        # output_file = codecs.open(output_filepath, 'w', 'UTF-8')
        # original_conll_file = codecs.open(dataset_filepaths[dataset_type], 'r', 'UTF-8')

        for i in range(len(token_indices)):
            feed_dict = {
                self.input_token_indices: token_indices[i],
                self.input_token_character_indices: character_indices_padded[i],
                self.input_token_lengths: token_lengths[i],
                self.input_token_patterns: pattern[i],
                self.dropout_keep_prob: 1.,
            }
            unary_scores, transition_params_trained = self.sess.run([self.unary_scores, self.transition_parameters],
                                                               feed_dict)
            #
            predictions, _ = tf.contrib.crf.viterbi_decode(unary_scores, transition_params_trained)
            # predictions = sess.run(self.predictions,feed_dict)
            predictions = predictions[1:-1]

            assert (len(predictions) == len(token_indices[i]))

            all_predictions.extend(predictions)
            all_y_true.extend(label_indices[i])

        label_predict = [vocab.labels[i] for i in all_predictions]
        label_true = [vocab.labels[i] for i in all_y_true]

        label_predict = utils_nlp.bioes_to_bio(label_predict)
        label_true = utils_nlp.bioes_to_bio(label_true)

        new_pre = []
        new_true = []
        for i in range(len(label_predict)):
            if label_true[i]!='O' or label_predict[i]!='O':
                new_pre.append(utils_nlp.remove_bio_from_label_name(label_predict[i]))
                new_true.append(label_true[i] if label_true[i]=='O' else label_true[i][2:])
        labels = [label if label=='O' else label[2:] for label in vocab.labels]
        labels = list(set(labels))
        report = classification_report(new_true,new_pre)

        print('evaluate',datatype)
        matrix  = confusion_matrix(new_true,new_pre,labels)
        file =codecs.open(datatype+'_evaluate.txt','w','utf-8')
        file.writelines(' '.join(labels)+'\n\r')
        for i,row in enumerate(matrix):
            file.writelines(' '.join([str(i) for i in row])+'\n\r')
        file.close()

        # print(matrix)
        print(report)
        return report

    def load_token_embedding(self,vocab,token_to_vector,dim):
        embedding = vocab.get_embedding(token_to_vector,dim)
        utils_tf.resize_tensor_variable(self.sess,self.token_embedding_weights,shape=embedding.shape)
        self.sess.run(self.token_embedding_weights.assign(embedding))

    def save_model(self,pathfile):
        self.saver.save(self.sess,pathfile)
    def load_model(self,pathfile):
        # utils_tf.resize_tensor_variable(sess, self.token_embedding_weights, [None, None])
        # utils_tf.resize_tensor_variable(sess, self.character_embedding_weights, [None, None])
        self.saver.restore(self.sess, pathfile)

        # self.graph = tf.get_default_graph()
        # self.predictions = self.graph.get_tensor_by_name('predictions:0')
    def update_model(self,sess,pathfile,vocab):
        # utils_tf.resize_tensor_variable(sess, self.token_embedding_weights, [None, None])
        # utils_tf.resize_tensor_variable(sess, self.character_embedding_weights, [None, None])
        self.saver.restore(sess, pathfile)
        token_embedding_weights = sess.run(self.token_embedding_weights.read_value())

    def export_model(self,sess,export_folder):
        builder = tf.saved_model.builder.SavedModelBuilder(export_folder)

        # Build the signature_def_map.

        tensor_input_token_indices = tf.saved_model.utils.build_tensor_info(self.input_token_indices)

        # tensor_input_label_indices_vector = tf.saved_model.utils.build_tensor_info(self.in)

        tensor_token_character_indices = tf.saved_model.utils.build_tensor_info(self.input_token_character_indices)

        tensor_input_token_lengths = tf.saved_model.utils.build_tensor_info(self.input_token_lengths)

        tensor_input_label_indices_flat = tf.saved_model.utils.build_tensor_info(self.input_label_indices_flat)

        tensor_dropout_keep_prob = tf.saved_model.utils.build_tensor_info(self.dropout_keep_prob)

        tensor_input_token_patterns = tf.saved_model.utils.build_tensor_info(self.input_token_patterns)

        # tensor_predictions = tf.contrib.crf.viterbi_decode(self.unary_scores,self.transition_parameters)[1:-1]
        tensor_unary_scores = tf.saved_model.utils.build_tensor_info(self.unary_scores)
        tensor_transitions = tf.saved_model.utils.build_tensor_info(self.transition_parameters)


        prediction_signature = (
            tf.saved_model.signature_def_utils.build_signature_def(
                inputs={
                    'input_token_indices': tensor_input_token_indices,
                    # 'input_label_indices_vector':tensor_input_label_indices_vector,
                    'token_character_indices': tensor_token_character_indices,
                    'input_token_lengths': tensor_input_token_lengths,
                    # 'input_label_indices_flat':tensor_input_label_indices_flat,
                    'dropout_keep_prob': tensor_dropout_keep_prob,
                    'input_token_patterns': tensor_input_token_patterns
                },
                outputs={
                    # 'predictions': tensor_predictions,
                    'unary_scores':tensor_unary_scores,
                    'transitions':tensor_transitions,
                },
                method_name=tf.saved_model.signature_constants.PREDICT_METHOD_NAME))


        legacy_init_op = tf.group(tf.tables_initializer(), name='legacy_init_op')
        builder.add_meta_graph_and_variables(
            sess, [tf.saved_model.tag_constants.SERVING],
            signature_def_map={
                'predictions':
                    prediction_signature,
                tf.saved_model.signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY:
                    prediction_signature,
            },
            legacy_init_op=legacy_init_op)

        builder.save()

        print('Done exporting!')