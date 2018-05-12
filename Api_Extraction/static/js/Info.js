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
        $("#addExperience").show();
        if(comparingResult_language_cv==0){
          $("#language_cv_selected").text("Select one!");
        }
        if(comparingResult_cpa==0){
          $("#cpa>span").text("Type your CPA here!");
        }
        if(comparingResult_major==0){
          $("#major>span").text("Type your major here!");
        }
        if(comparingResult_name==0||personal_Details_name==""){
          $("#personal_Details_name").text("No name. Let's add one!");
        }
        if(comparingResult_birthday==0){
          $("#birthday>span").text("Type your birthday here!");
        }
        if(comparingResult_address==0){
          $("#address>span").text("Type your address here!");
        }
        if(comparingResult_mail==0){
          $("#mail>span").text("Type your mail address here!");
        }
        if(comparingResult_phone==0){
          $("#phone>span").text("Type your phone number here!");
        }
        if(comparingResult_applyingPosition==0){
          $("#applyingPosition>span").text("Type your applying position here!");
        }
        if(comparingResult_edu_time==0){
          $("#edu_time>span").text("Type your learning period here!");
        }
        if(comparingResult_university==0){
          $("#university>span").text("Type your university here!");
        }
        if(comparingResult_exp_time==0){
          $(".exp_time>span").text("Type your company here!");
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
        if(comparingResult_sex==0){
          $("#sex_selected").text("Select one!");
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
          $("#skill_programming").text("Type your programming skills here!");
        }
        if(skill_language==""){
          $("#skill_language").text("Type your language skills here!");
        }
        if(skill_description==""){
          $("#skill_description").text("Type your description here!");
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
        $("#addExperience").hide();
    });
    // handle Add Experience event
    $("#addExperience").click(function(){
      $("#addClassExperience").show();
    })
    // handle upload photo event
    $(function(){
    $("#changePhoto").on('click', function(e){
        e.preventDefault();
        $("#upload-photo:hidden").trigger('click');
    });
    });
    // handle null data
    var pattern="[";
    //language_cv
    var language_cv= $( "#language_cv_selected" ).text();
    
    
    if(language_cv!=""){
      var language_cvInShort=language_cv[0]
      var comparingResult_language_cv = language_cvInShort.localeCompare(pattern);
      if(comparingResult_language_cv==0){
      $("#language_cv_selected").text("No data.");
      }

    } else{
      $("#language_cv_selected").text("No data. Select one!")
    }
    //sex
    var sex= $( "#sex_selected" ).text();
    
    console.log(sex);
    if(sex!=""){
      var sexInShort=sex[0]
      var comparingResult_sex = sexInShort.localeCompare(pattern);
      if(comparingResult_sex==0){
      $("#sex_selected").text("No data.");
      }
    } else{
      $("#sex_selected").text("No data. Select one!")
    }

    //cpa:
    var cpa= $( "#cpa" ).text();
   
    
    if(cpa!=""){
          var cpaInShort=cpa[0];
          var comparingResult_cpa = cpaInShort.localeCompare(pattern);
          if(comparingResult_cpa==0){
          $("#cpa,#CPA").hide();
          }
    }else{
      $("#cpa").append("No data. Let's update your CPA!")
    }
    //name:
    var personal_Details_name= $( "#personal_Details_name" ).text();
    
    if(personal_Details_name!=""){
      var nameInShort=personal_Details_name[0];
      var comparingResult_name = nameInShort.localeCompare(pattern);
      if(comparingResult_name==0){
      $("#personal_Details_name").text("No name. Let's add one!");
      }
    } else{
      $("#personal_Details_name").text("No name. Let's add one!");
    }
    //birthday:
    var birthday= $( "#birthday" ).text();

    if(birthday!=""){
      var birthdayInShort=birthday[0];
      var comparingResult_birthday = birthdayInShort.localeCompare(pattern);
      if(comparingResult_birthday==0){
        $("#birthday").hide();
      }
    } else{
      $("#birthday").text("No data. Let's update your birthday!")
    }
    //address:
    var address= $( "#address" ).text();
    
    if(address!=""){
      var addressInShort=address[0];
      var comparingResult_address = addressInShort.localeCompare(pattern);
      if(comparingResult_address==0){
        $("#address").hide();
      }
    } else{
      $("#address").text("No data. Let's update your address!");
    }
    //mail:
    var mail= $( "#mail" ).text();
    if(mail!=""){
      var mailInShort=mail[0];
      var comparingResult_mail = mailInShort.localeCompare(pattern);
      if(comparingResult_mail==0){
        $("#mail").hide();
      }
    } else{
      $("#mail").append("No data. Let's update your mail address!")
    }
    //phone:
    var phone= $( "#phone" ).text();
    if(phone!=""){
      var phoneInShort=phone[0];
      var comparingResult_phone = phoneInShort.localeCompare(pattern);
      if(comparingResult_phone==0){
        $("#phone").hide();
      }
    } else{
      $("#phone").append("No data. Let's update your phone number!")
    }
    //applyingPosition:
    var applyingPosition= $( "#applyingPosition" ).text();
    if(applyingPosition!=""){
      var applyingPositionInShort=applyingPosition[0];
      var comparingResult_applyingPosition = applyingPositionInShort.localeCompare(pattern);
      if(comparingResult_applyingPosition==0){
        $("#applyingPosition").hide();
      }
    } else{
      $("#applyingPosition").append("No data.Let's update your applying position!")
    }
    //edu_time:
    var edu_time= $( "#edu_time" ).text();
    if(edu_time!=""){
      var edu_timeInShort=edu_time[0];
      var comparingResult_edu_time = edu_timeInShort.localeCompare(pattern);
      if(comparingResult_edu_time==0){
        $("#edu_time").hide();
      }
    } else{
      $("#edu_time").append("No data. Let's update your learning period!");
    }
    //university:
    var university= $( "#university" ).text();
    if(university!=""){
      var universityInShort=university[0];
      var comparingResult_university = universityInShort.localeCompare(pattern);
      if(comparingResult_university==0){
        $("#university,#UNIVERSITY").hide();
      }
    } else{
      $("#edu_time").append("No data. Let's update your university!");
    }
    //major:
    var major= $( "#major" ).text();
    if(major!=""){
      var majorInShort=major[0];
      var comparingResult_major = majorInShort.localeCompare(pattern);
      if(comparingResult_major==0){
        $("#major,#MAJOR").hide();
      }
    } else{
      $("#major").append("No data. Let's update your major!");
    }
    //exp_time:
    var exp_time= $( ".exp_time" ).text();
    if(exp_time!=""){
      var exp_timeInShort=exp_time[0];
      var comparingResult_exp_time = exp_timeInShort.localeCompare(pattern);
      if(comparingResult_exp_time==0){
        $(".exp_time").hide();
      }
    } else{
      $(".exp_time").append("No data. Let's update your working period!");
    }
    //company:
    var company= $( ".company" ).text();
    if(company!=""){
      var companyInShort=company[0];
      var comparingResult_company = companyInShort.localeCompare(pattern);
      if(comparingResult_company==0){
        $(".company").hide();
      }
    } else{
      $(".company").append("No data. Let's update your company!");
    }
    //position:
    var position= $( ".position" ).text();
    if(position!=""){
      var positionInShort=position[0];
      var comparingResult_position = positionInShort.localeCompare(pattern);
      if(comparingResult_position==0){
        $(".position").hide();
      }
    } else{
      $(".position").append("No data. Let's update your working position!");
    }
    //programming:
    var programming= $( ".programming" ).text();
    if (programming!="") {
      var programmingInShort=programming[0];
      var comparingResult_programming = programmingInShort.localeCompare(pattern);
      if(comparingResult_programming==0){
        $(".programming").hide();
      }
    }else {
      $(".programming").append("No data. Let's update your programming language!");
    }
    //project:
    var project= $( ".project" ).text();
    if (project!="") {
      var projectInShort=project[0];
      var comparingResult_project = projectInShort.localeCompare(pattern);
      if(comparingResult_project==0){
        $(".project").hide();
      }
    } else{
      $(".project").append("No data. Let's update your projects here!");
    }
    //description:
    var description= $( ".description" ).text();
    if(description!=""){
      var descriptionInShort=description[0];
      var comparingResult_description = descriptionInShort.localeCompare(pattern);
      if(comparingResult_programming==0){
        $(".description").hide();
      }
    } else{
      $(".description").append("No data. Let's update your programming language!");
    }
    //skill_programming:
    var skill_programming= $( "#skill_programming" ).text();
    
    console.log(skill_programming);
    if(skill_programming!=""){
      var skill_programmingInShort=skill_programming[0];
      var comparingResult_skill_programming = skill_programmingInShort.localeCompare(pattern);
      if(comparingResult_skill_programming==0){
        $("#skill_programming").hide();
      }
    }else{
      $("#skill_programming").append("No data. Let's update your programming skills!");
    }
    //skill_language:
    var skill_language= $( "#skill_language" ).text();
    if(skill_language!=""){
      var skill_languageInShort=skill_language[0];
      var comparingResult_skill_language = skill_languageInShort.localeCompare(pattern);
      if(comparingResult_skill_language==0){
        $("#skill_language").hide();
      }
    } else{
      $("#skill_language").append("No data. Let's update your language skills here!");
    }
    //skill_description:
    var skill_description= $( "#skill_description" ).text();
    if(skill_description!=""){
      var skill_descriptionInShort=skill_description[0]+skill_description[1]+ skill_description[skill_description.length-2]+skill_description[skill_description.length-1]
      var comparingResult_skill_description = skill_descriptionInShort.localeCompare(pattern);
      if(comparingResult_skill_description==0){
        $("#skill_description").hide();
      }
    } else{
      $("#skill_description").append("No data. Let's update a description for your skills!");
    }
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