feedBack = document.querySelector('.success-message');

if(feedBack){
    setTimeout(function() {
        $(feedBack).fadeOut('fast');
    }, 1500); // <-- time in milliseconds
}

date = new Date();

password_box = document.querySelector('#password');
error_msg = document.querySelectorAll('.show-error');

for(em of error_msg){
    em.classList.remove('show-error');
}

male_div = document.querySelector('.male-div');
female_div = document.querySelector('.female-div');
others_div = document.querySelector('.others-div');

male_radio = document.querySelector('#male');
female_radio = document.querySelector('#female');
others_radio = document.querySelector('#others');

if(male_div && female_div && others_div){
    gender_div = [male_div, female_div, others_div];

    gender_div.forEach((div) => {
        div.addEventListener('click', () => {
            for(sex_div of gender_div){
                sex_div.classList.remove('selected-gender');
            }

            if(div == male_div){
                male_radio.checked = true;
            }

            else if(div == female_div){
                female_radio.checked = true;
            }

            if(div == others_div){
                others_radio.checked = true;
            }

            div.classList.add('selected-gender');
        });
    });
}


var selectedFile;
var input = document.querySelector("#upload-profile-button");
var profile_image_error = document.querySelector('.profile-image-error');
input.addEventListener('change', updateImageDisplay);


function updateImageDisplay() {
    imageExtension = ['jpg', 'jpeg', 'png']
    extension = input.files[0]['name'].split('.')[1]

    if(!imageExtension.includes(extension)){
        input.value = null;
    }

    if(input.files.length != 0){
        document.querySelector('.user-image').src = window.URL.createObjectURL(input.files[0])
    }

    if(input.files.length == 0) {
        input.files = selectedFile;
        profile_image_error.classList.add('show-error');

        setTimeout(function() {
            $(profile_image_error).removeClass('show-error');

        }, 2000);
    }

    else {
        selectedFile = input.files;
        profile_image_error.classList.remove('show-error');
   }
}


function validateForm(){
    success = true;
    email_regex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/i;
    password_regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;

    dob_day = document.querySelector('#dob-day');
    genderDiv = document.querySelector('.gender');
    dob_year = document.querySelector('#dob-year');
    dob_month = document.querySelector('#dob-month');
    fullNameArea = document.querySelector('#full_name');

    dob_error = document.querySelector('.dob-error');
    gender_error = document.querySelector('.gender-error');
    password_error = document.querySelector('.password-error');
    fullNameError = document.querySelector('.full-name-error');
    email_error = document.querySelector('.signup-email-error');

    password = password_box.value;
    email = document.querySelector('#email').value;

    if(fullNameArea){
        fullNameValue = fullNameArea.value.trim();

        if(!fullNameValue){
            success = false;
            fullNameError.classList.add('show-error');
            fullNameError.innerText = 'This field must not be empty';
        }

        else{
            fullNameError.classList.remove('show-error');
        }
    }

    if(!email_regex.test(email)){
        success = false;
        email_error.classList.add('show-error');
        email_error.innerText = "Invalid Email";
    }

    else{
        email_error.classList.remove('show-error');
    }

    if(password_regex.test(password) == false){
        success = false;
        password_error.classList.add('show-error');
        password_error.innerText = "Password must be a combination of letters, numbers, and special characters, with a minimum length of 8 characters"
    }

    else{
        password_error.classList.remove('show-error');
    }

    if(dob_year && dob_month && dob_day){
        dob_day_value = dob_day.value;
        dob_year_value = dob_year.value;
        dob_month_value = dob_month.value;

        if(!dob_day_value || !dob_month_value || !dob_year_value ||
        isNaN(parseInt(dob_day_value)) || isNaN(parseInt(dob_month_value)) || isNaN(parseInt(dob_year_value)) ||
        !(dob_day_value > 0 && dob_day_value < 32) || !(dob_month_value > 0 && dob_month_value < 13) ||
        !(dob_year_value >= 1920 && dob_year_value <= date.getFullYear())){
            success = false;
            dob_error.classList.add('show-error');
            dob_error.innerText = 'Invalid Date of Birth';
            }

        else{
            dob_error.classList.remove('show-error');
        }
    }

    selected_gender = '';

    if(genderDiv){
        for(genderDiv of gender_div){
            if(genderDiv.classList.contains('selected-gender')){
                selected_gender = genderDiv;
            }
        }

        if(selected_gender){
            gender_error.classList.remove('show-error');
        }

        else{
            success = false;
            gender_error.classList.add('show-error');
            gender_error.innerText = 'Select any one';
        }
    }

    return success == true;
}
