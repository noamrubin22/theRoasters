import main
import csv
from main import schedule
from scorefunction import calcScore
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session


def print_schedule():

    schedule_location = "visualisation/schedule.csv"
    schedule_file = open(schedule_location, 'w')

    writer = csv.writer(schedule_file)

    times = ['Monday, 09:00 - 11:00', 'Monday, 11:00 - 13:00', 'Monday, 13:00 - 15:00', 'Monday, 15:00 - 17:00',
             'Tuesday, 09:00 - 11:00', 'Tuesday, 11:00 - 13:00', 'Tuesday, 13:00 - 15:00', 'Tuesday, 15:00 - 17:00',
             'Wednesday, 09:00 - 11:00', 'Wednesday, 11:00 - 13:00', 'Wednesday, 13:00 - 15:00', 'Wednesday, 15:00 - 17:00',
             'Thursday, 09:00 - 11:00', 'Thursday, 11:00 - 13:00', 'Thursday, 13:00 - 15:00', 'Thursday, 15:00 - 17:00',
             'Friday, 09:00 - 11:00', 'Friday, 11:00 - 13:00', 'Friday, 13:00 - 15:00', 'Friday, 15:00 - 17:00']

    timetable = []

    j = 0

    for i in range(0, len(schedule), 7):
        timelock = []
        timelock.append(times[j])
        timelock.append(schedule[i])
        timelock.append(schedule[i+1])
        timelock.append(schedule[i+2])
        timelock.append(schedule[i+3])
        timelock.append(schedule[i+4])
        timelock.append(schedule[i+5])
        timelock.append(schedule[i+6])
        timetable.append(timelock)
        j += 1

    score = calcScore(main.allcourses, main.student_list, main.chambers)
    fields = ['Score = {}'.format(score), 'A1.04', 'A1.06', 'A1.08', 'A1.10', 'B0.201', 'C0.110', 'C1.112']

    writer.writerow(fields)

    for timelock in timetable:
        writer.writerow(timelock)

    print("Printed a schedule at {} with a score of {}.".format(schedule_location, score))

for i in range(4):
    print_schedule()
