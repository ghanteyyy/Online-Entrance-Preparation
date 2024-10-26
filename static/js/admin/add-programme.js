function validateForm(){
    success = true;

    subject_list_value = document.querySelector('#subjects_list').value.trim();
    programme_name_value = document.querySelector('#programme_name').value.trim();
    total_question_to_retrieve = document.querySelector('#total_question_to_retrieve').value.trim();

    subjectError = document.querySelector('.subject-error');
    programmeError = document.querySelector('.programme-error');
    totalQuestionToRetrieveError = document.querySelector('.total-question-error');
    subQuesNumError = document.querySelector('.sub-ques-num-error');

    if(!programme_name_value){
        success = false;
        programmeError.classList.add('show-error');
    }

    else{
        programmeError.classList.remove('show-error');
    }

    if(!subject_list_value){
        success = false;
        subjectError.classList.add('show-error');
    }

    else{
        subjectError.classList.remove('show-error');
    }

    if(!total_question_to_retrieve){
        success = false;
        totalQuestionToRetrieveError.classList.add('show-error');
    }

    else{
        totalQuestionToRetrieveError.classList.remove('show-error');
    }

    if(subject_list_value && total_question_to_retrieve){
        if(subject_list_value.split(',').length != total_question_to_retrieve.split(',').length){
            success = false;
            subQuesNumError.classList.add('show-error');
        }

        else{
            subQuesNumError.classList.remove('show-error');
        }
    }

    return success == true;
}
