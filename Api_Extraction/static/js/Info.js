$(document).ready(function(){
        // var country_list = [{"name":"Afghanistan"},{"name":"Brazil"},{"name":"Belgium"},{"name":"Costa Rica"},{"name":"France"},{"name":"Zimbabwe"}];
        // $("#personal_Details").mirandajs(country_list);
	$("#personal_Details_name").mirandajs(myData,{jsonNode:['person_details']});
	$("#personal_Details").mirandajs(myData,{jsonNode:['person_details']});
	$("#language_cv").mirandajs(myData);
	$("#education").mirandajs(myData,{jsonNode:['education']});
	$("#experience").mirandajs(myData, {jsonNode:['experience']});
  $("#skill").mirandajs(myData,{jsonNode:['skill']});
	  var myAwards = myData.awards;
          //console.log(myObject);
          for (i in myAwards) {
              $("#awards").append("<li>"+myAwards[i]);
          }
    var myOthers = myData.other;
          //console.log(myObject);
          for (i in myOthers) {
              $("#checkOthers>li").append(myOthers[i]);
          }
    var myObjective = myData.objective;
          //console.log(myObject);
          for (i in myObjective) {
              $("#objective>li").append(myObjective[i]);
          }
    var myHobbies = myData.hobbi;
          //console.log(myObject);
          for (i in myHobbies) {
              $("#checkHobbies>li").append(myHobbies[i]);
          }
    // handle editting info
    $("#editInfo").click(function(){
        $("p,#personal_Details_name,h5,h6,li,#skill_programming,#skill_language,#skill_description").attr('contenteditable','true');
        $("p,#personal_Details_name,h5,h6,li,p").css("color","#000");
        $("#personal_Details_name").css("color","white");
        $("#saveInfo,#changePhoto,#hr_line").show();
        $(this).hide();
        $("#CPA,#MAJOR,#UNIVERSITY,.skills_title").attr('contenteditable','false');
        $("#language_cv_select").prop('disabled', false);
        $("#sex").prop('disabled', false);
        $("#language_cv,#personal_Details_name,#phone,#birthday,#address,#sex,#mail,#applyingPosition,#edu_time,#major,#university,.exp_time,.project,.company,.position,.programming,.skills_title,#skill_programming,#skill_language,#skill_description,.li_hobbies,.li_others,.li_objective,#cpa,#CPA").show();
        
        if(comparingResult_language_cv==0){
          $("#language_cv_selected").text("Select one!");
        }
        if(comparingResult_cpa==0){
          $("#cpa").append("Type your CPA here!");
        }
        if(comparingResult_name==0||personal_Details_name==""){
          $("#personal_Details_name").text("No name. Let's add one!");
        }
        if(comparingResult_birthday==0){
          $("#birthday").append("Type your birthday here!");
        }
        if(comparingResult_address==0){
          $("#address").append("Type your address here!");
        }
        if(comparingResult_mail==0){
          $("#mail").append("Type your mail address here!");
        }
        if(comparingResult_phone==0){
          $("#phone").append("Type your phone number here!");
        }
        if(comparingResult_applyingPosition==0){
          $("#applyingPosition").append("Type your applying position here!");
        }
        if(comparingResult_edu_time==0){
          $("#edu_time").append("Type your learning period here!");
        }
        if(comparingResult_university==0){
          $("#university,#UNIVERSITY").append("Type your university here!");
        }
        if(comparingResult_exp_time==0){
          $(".exp_time").text("Type your company here!");
        }
        if(comparingResult_position==0){
          $(".position").text("Type your working position here!");
        }
        if(comparingResult_programming==0){
          $(".programming").text("Type your programming language here!");
        }
        if(comparingResult_project==0){
          $(".project").text("Type your projects here!");
        }
        if(comparingResult_programming==0){
          $(".description").text("Type your programming language here!");
        }
        if(li_OthersContent==""){
          $(".li_others").text("Type something here!");
        }
        if(li_HobbiesContent==""){
          $(".li_hobbies").text("Write some hobbies here!");
        }
        if(li_ObjectiveContent==""){
          $(".li_objective").text("Write your objective here!");
        }
        if(skill_programming==""){
          $("#skill_programming").append("Type your programming skills here!");
        }
        if(skill_language==""){
          $("#skill_language").append("Type your language skills here!");
        }
        if(skill_description==""){
          $("#skill_description").append("Type your description here!");
        }
    });
    //handle saving data
    $("#saveInfo").click(function(){
        $("p,#personal_Details_name,h5,h6,li").attr('contenteditable','false');
        $("p,#personal_Details_name,h5,h6,li,p").css("color","#757575");
        $("#personal_Details_name").css("color","#757575");
        $("#editInfo").show();
        $("#saveInfo,#changePhoto,#hr_line").hide();
        $("#language_cv_select").prop('disabled', true);
        $("#sex").prop('disabled', true);
    });
    // handle upload photo event
    $(function(){
    $("#changePhoto").on('click', function(e){
        e.preventDefault();
        $("#upload-photo:hidden").trigger('click');
    });
    });
    // handle null data
    var pattern="[[]]";
    //language_cv
    var language_cv= $( "#language_cv_selected" ).text();
    var language_cvInShort=language_cv[0]+language_cv[1]+ language_cv[language_cv.length-2]+language_cv[language_cv.length-1]
    var comparingResult_language_cv = language_cvInShort.localeCompare(pattern);
    console.log(language_cv);
    if(comparingResult_language_cv==0){
      $("#language_cv_selected").hide();
    }
    if(language_cv==""){
      $("#language_cv_selected").text("Select one!")
    }
    //cpa:
    var cpa= $( "#cpa" ).text();
    var cpaInShort=cpa[0]+cpa[1]+ cpa[cpa.length-2]+cpa[cpa.length-1]
    var comparingResult_cpa = cpaInShort.localeCompare(pattern);
    if(comparingResult_cpa==0){
      $("#cpa,#CPA").hide();
    }
    if(cpa==""){
      $("#cpa").append("Type your CPA here!")
    }
    //name:
    var personal_Details_name= $( "#personal_Details_name" ).text();
    var nameInShort=personal_Details_name[0]+personal_Details_name[1]+ personal_Details_name[personal_Details_name.length-2]+personal_Details_name[personal_Details_name.length-1]
    var comparingResult_name = nameInShort.localeCompare(pattern);
    if(comparingResult_name==0||personal_Details_name==""){
      $("#personal_Details_name").text("No name. Let's add one!");
    }
    //birthday:
    var birthday= $( "#birthday" ).text();
    var birthdayInShort=birthday[0]+birthday[1]+ birthday[birthday.length-2]+birthday[birthday.length-1]
    var comparingResult_birthday = birthdayInShort.localeCompare(pattern);
    if(comparingResult_birthday==0){
      $("#birthday").hide();
    }
    if(birthday==""){
      $("#birthday").append("Type your birthday here!")
    }
    //address:
    var address= $( "#address" ).text();
    var addressInShort=address[0]+address[1]+ address[address.length-2]+address[address.length-1]
    var comparingResult_address = addressInShort.localeCompare(pattern);
    if(comparingResult_address==0){
      $("#address").hide();
    }
    if(address==""){
      $("#address").append("Type your address here!");
    }
    //mail:
    var mail= $( "#mail" ).text();
    var mailInShort=mail[0]+mail[1]+ mail[mail.length-2]+mail[mail.length-1]
    var comparingResult_mail = mailInShort.localeCompare(pattern);
    if(comparingResult_mail==0){
      $("#mail").hide();
    }
    if(mail==""){
      $("#mail").append("Type your mail address here!")
    }
    //phone:
    var phone= $( "#phone" ).text();
    var phoneInShort=phone[0]+phone[1]+ phone[phone.length-2]+phone[phone.length-1]
    var comparingResult_phone = phoneInShort.localeCompare(pattern);
    if(comparingResult_phone==0){
      $("#phone").hide();
    }
    if(phone==""){
      $("#phone").append("Type your phone number here!")
    }
    //applyingPosition:
    var applyingPosition= $( "#applyingPosition" ).text();
    var applyingPositionInShort=applyingPosition[0]+applyingPosition[1]+ applyingPosition[applyingPosition.length-2]+applyingPosition[applyingPosition.length-1]
    var comparingResult_applyingPosition = applyingPositionInShort.localeCompare(pattern);
    if(comparingResult_applyingPosition==0){
      $("#applyingPosition").hide();
    }
    if(applyingPosition==""){
      $("#applyingPosition").append("Type your applying position here!")
    }
    //edu_time:
    var edu_time= $( "#edu_time" ).text();
    var edu_timeInShort=edu_time[0]+edu_time[1]+ edu_time[edu_time.length-2]+edu_time[edu_time.length-1]
    var comparingResult_edu_time = edu_timeInShort.localeCompare(pattern);
    if(comparingResult_edu_time==0){
      $("#edu_time").hide();
    }
    if(edu_time==""){
      $("#edu_time").append("Type your learning period here!");
    }
    //university:
    var university= $( "#university" ).text();
    var universityInShort=university[0]+university[1]+ university[university.length-2]+university[university.length-1]
    var comparingResult_university = universityInShort.localeCompare(pattern);
    if(comparingResult_university==0){
      $("#university,#UNIVERSITY").hide();
    }
    if(university==""){
      $("#edu_time").append("Type your university here!");
    }
    //major:
    var major= $( "#major" ).text();
    var majorInShort=major[0]+major[1]+ major[major.length-2]+major[major.length-1]
    var comparingResult_major = majorInShort.localeCompare(pattern);
    if(comparingResult_major==0){
      $("#major,#MAJOR").hide();
    }
    if(major==""){
      $("#major").append("Type your major here!");
    }
    //exp_time:
    var exp_time= $( ".exp_time" ).text();
    var exp_timeInShort=exp_time[0]+exp_time[1]+ exp_time[exp_time.length-2]+exp_time[exp_time.length-1]
    var comparingResult_exp_time = exp_timeInShort.localeCompare(pattern);
    if(comparingResult_exp_time==0){
      $(".exp_time").hide();
    }
    if(exp_time==""){
      $(".exp_time").append("Type your working period here!");
    }
    //company:
    var company= $( ".company" ).text();
    var companyInShort=company[0]+company[1]+ company[exp_time.length-2]+company[company.length-1]
    var comparingResult_company = companyInShort.localeCompare(pattern);
    if(comparingResult_company==0){
      $(".company").hide();
    }
    if(company==""){
      $(".company").append("Type your company here!");
    }
    //position:
    var position= $( ".position" ).text();
    var positionInShort=position[0]+position[1]+ position[position.length-2]+position[position.length-1]
    var comparingResult_position = positionInShort.localeCompare(pattern);
    if(comparingResult_position==0){
      $(".position").hide();
    }
    if(position==""){
      $(".position").append("Type your working position here!");
    }
    //programming:
    var programming= $( ".programming" ).text();
    var programmingInShort=programming[0]+programming[1]+ programming[programming.length-2]+programming[programming.length-1]
    var comparingResult_programming = programmingInShort.localeCompare(pattern);
    if(comparingResult_programming==0){
      $(".programming").hide();
    }
    if(programming==""){
      $(".programming").append("Type your programming language here!");
    }
    //project:
    var project= $( ".project" ).text();
    var projectInShort=project[0]+project[1]+ project[project.length-2]+project[project.length-1]
    var comparingResult_project = projectInShort.localeCompare(pattern);
    if(comparingResult_project==0){
      $(".project").hide();
    }
    if(project==""){
      $(".project").append("Type your projects here!");
    }
    //description:
    var description= $( ".description" ).text();
    var descriptionInShort=description[0]+description[1]+ description[description.length-2]+description[description.length-1]
    var comparingResult_description = descriptionInShort.localeCompare(pattern);
    if(comparingResult_programming==0){
      $(".description").hide();
    }
    if(programming==""){
      $(".description").append("Type your programming language here!");
    }
    //skill_programming:
    var skill_programming= $( "#skill_programming" ).text();
    var skill_programmingInShort=skill_programming[0]+skill_programming[1]+ skill_programming[skill_programming.length-2]+skill_programming[skill_programming.length-1];
    // var comparingResult_skill_programming = skill_programmingInShort.localeCompare(pattern);
    console.log(skill_programming);
    // if(comparingResult_skill_programming==0){
    //   $("#skill_programming").hide();
    // }
    // if(skill_programming==""){
    //   $("#skill_programming").append("Type your programming skills here!");
    // }
    //skill_language:
    var skill_language= $( "#skill_language" ).text();
    //var skill_languageInShort=skill_language[0]+skill_language[1]+ skill_language[skill_language.length-2]+skill_language[skill_language.length-1]
    // var comparingResult_skill_language = skill_languageInShort.localeCompare(pattern);
    // if(comparingResult_skill_language==0){
    //   $("#skill_language").hide();
    // }
    // if(skill_language==""){
    //   $("#skill_language").append("Type your language skills here!");
    // }
    //skill_description:
    var skill_description= $( "#skill_description" ).text();
    // var skill_descriptionInShort=skill_description[0]+skill_description[1]+ skill_description[skill_description.length-2]+skill_description[skill_description.length-1]
    // var comparingResult_skill_description = skill_descriptionInShort.localeCompare(pattern);
    // if(comparingResult_skill_description==0){
    //   $("#skill_description").hide();
    // }
    // if(skill_description==""){
    //   $("#skill_description").append("Type your a description for your skills here!");
    // }
    // checkOthers:
    var li_OthersContent= $( "#checkOthers>.li_others" ).text();
    if(li_OthersContent==""){
      $(".li_others").hide();
    }
    //checkHobbies
    var li_HobbiesContent= $( "#checkHobbies>.li_hobbies" ).text();
    if(li_HobbiesContent==""){
      $(".li_hobbies").hide();
    }
    //checkObjective
    var li_ObjectiveContent= $( "#objective>.li_objective" ).text();
    if(li_ObjectiveContent==""){
      $(".li_objective").hide();
    }
});