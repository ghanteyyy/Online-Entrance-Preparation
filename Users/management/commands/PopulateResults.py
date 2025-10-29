import random
import requests
from django.core.management.base import BaseCommand
from Users.models import *


class PopulateResults:
    def __init__(self, Prog, Email, NumberOfResultsToGenerate):
        self.Email = Email
        self.Programme = Prog
        self.NumberOfResultsToGenerate = NumberOfResultsToGenerate

        self.UsersObj = CustomUser.objects.filter(email=self.Email).first()

    def GetSubjects(self, programme):
        SubjectsID = []
        ProgrammeObj = Programme.objects.filter(Name=programme).first()

        for id in Subject.objects.filter(ProgrammeID=ProgrammeObj):
            SubjectsID.append(id)

        return SubjectsID

    def Action(self):
        if self.Programme == 'Random':
            all_programmes = Programme.objects.all()
            programmes = [random.choice(all_programmes) for _ in range(self.NumberOfResultsToGenerate)]

        else:
            programme = self.Programme.Name
            allSubjects = self.GetSubjects(self.Programme)

        for i in range(self.NumberOfResultsToGenerate):
            correct_counter = 0

            if self.Programme == 'Random':
                programme = programmes[i].Name
                allSubjects = self.GetSubjects(programme)

            results = Exams(UserID=self.UsersObj, ProgrammeName=programme)
            results.save()

            for subject in allSubjects:
                total_questions_per_subject = subject.TotalQuestionsToSelect
                number_of_correct_answers_to_select = random.randint(1, total_questions_per_subject)

                correct_counter += number_of_correct_answers_to_select

                questions = list(Questions.objects.filter(SubjectID=subject.ID))
                random.shuffle(questions)

                for question in questions:
                    wrong_or_right = random.SystemRandom().choice([0, 1])

                    if number_of_correct_answers_to_select > 0 and wrong_or_right:
                        user_answer = question.Answer
                        number_of_correct_answers_to_select -= 1

                    else:
                        choices = [question.OptionOne, question.OptionTwo, question.OptionThree, question.OptionFour]
                        choices = [choice for choice in choices if choice != question.Answer]
                        user_answer = random.choice(choices)

                    result_details = ResultDetails(
                                        ResultID = results,
                                        QuestionID = question,
                                        UserAnswer = user_answer
                                    )

                    result_details.save()

                results.CorrectCounter = correct_counter
                results.save()

            resultExtraDetails = ResultsExtraDetails.objects.get_or_create(UserID=self.UsersObj)[0]

            if programme.lower() == 'bca':
                resultExtraDetails.BCA += 1

            elif programme.lower() == 'bit':
                resultExtraDetails.BIT += 1

            elif programme.lower() == 'bim':
                resultExtraDetails.BIM += 1

            elif programme.lower() == 'bscsit':
                resultExtraDetails.BSCSIT += 1

            resultExtraDetails.TestsTaken += 1
            resultExtraDetails.save()


class Command(BaseCommand):
    def GetAllProgrammes(self):
        programmes = dict()

        for index, programme in enumerate(Programme.objects.all()):
            programmes.update({
                str(index + 1): programme
            })

        programmes[str(index + 2)] = 'Random'

        return programmes

    def GetEmail(self):
        while True:
            email = input("Enter user's email: ")

            if email.lower() == 'all':
                return email.lower()

            if CustomUser.objects.filter(email__iexact=email):
                return email

            else:
                print('\nEmail not found ...\n')

    def GetProgramme(self):
        menu_list = ''
        ProgramMaps = self.GetAllProgrammes()

        for key, value in ProgramMaps.items():
            menu_list += f'\t{key}. {value}\n'

        while True:
            print("Choose any one of the following: ")
            print(menu_list)

            programme = input("Enter Options: ")

            if programme in ProgramMaps:
                return ProgramMaps[programme]

            else:
                print('\nInvalid option ...\n')

    def GetNumberOfResults(self):
        while True:
            numberOfResults = input("Enter the number of results to generate: ")

            if numberOfResults.isdigit() is False:
                print('Number was expected ...\n')

            else:
                return int(numberOfResults)

    def _create_tags(self):
        email = self.GetEmail()

        if email == 'all':
            emails = CustomUser.objects.filter(is_superuser=False)

            for index, email in enumerate(emails):
                numberOfResults = random.SystemRandom().randint(60, 80)

                print(f"Populating Results for: {email} ... {index + 1}/{len(emails)}")
                PopulateResults("Random", email, numberOfResults).Action()

        else:
            programme = self.GetProgramme()
            numberOfResults = self.GetNumberOfResults()
            PopulateResults(programme, email, numberOfResults).Action()

    def handle(self, *args, **options):
        self._create_tags()
