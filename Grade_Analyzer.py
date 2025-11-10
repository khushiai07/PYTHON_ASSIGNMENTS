import csv

def checkGrade():
    print('----M is manual and F is file---')
    default = input('Enter the method (M or F):').lower()

    if default == 'f':
        with open('grade.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row['name']
                subject = row['subject']
                grade = int(row['grade'])

                if grade >= 90:
                    letter = 'A'
                elif grade >= 80:
                    letter = 'B'
                elif grade >= 70:
                    letter = 'C'
                else:
                    letter = 'D'

                print(f"{name} scored {grade} ({letter}) in {subject}")

    elif default == 'm':
        data = []

        while True:
            print('----Kindly enter the data----')
            name = input('Enter a name: ')
            subject = input('Enter the Subject: ')
            grade = int(input('Enter the respective grade: '))

            data.append({
                'name': name,
                'subject': subject,
                'grade': grade
            })

            moreData = input('Would you like to enter more data (Y or N): ').lower()
            if moreData == 'n':
                break

        # Display results
        for entry in data:
            name = entry['name']
            subject = entry['subject']
            grade = entry['grade']

            if grade >= 90:
                letter = 'A'
            elif grade >= 80:
                letter = 'B'
            elif grade >= 70:
                letter = 'C'
            else:
                letter = 'D'

            print(f"{name} scored {grade} ({letter}) in {subject}")

    else:
        print('Error — kindly check the values entered.')
        checkGrade()


checkGrade()
