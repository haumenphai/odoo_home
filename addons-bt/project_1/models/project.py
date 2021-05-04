# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date, datetime, timedelta
import calendar



class ProjectTask(models.Model):
    _inherit = 'project.task'
    start_date = fields.Date(string='Start Date')
    task_repeat = fields.Selection([('no', 'No'), ('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')],
                                   string='Task Repeat', default='no', required=True)
    day_of_week = fields.Selection([('0', 'Monday'),
                                    ('1', 'Tuesday'),
                                    ('2', 'Wednesday'),
                                    ('3', 'Thursday'),
                                    ('4', 'Friday'),
                                    ('5', 'Saturday'),
                                    ('6', 'Sunday'),
                                    ], default='0', string="Day of week")
    day_of_month = fields.Integer(sting="Day of month", default=1)

    @api.constrains('day_of_month')
    def _check_day_of_month(self):
        for r in self:
            if r.day_of_month < 1 or r.day_of_month > 31:
                raise ValidationError(" 1 <= 'Day of month' <= 31 ")

    def write(self, vals):
        print(self.user_id.name)
        print(self.env.user.name)
        return super(ProjectTask, self).write(vals)

    def unlink(self):
        print('unlink')

    def create_task_repeat(self):
        tasks_reapeat = self.search([('task_repeat', '!=', 'no')])
        last_day = calendar.monthrange(date.today().year, date.today().month)[1]

        list_create = []
        for r in tasks_reapeat:
            if not (r.date_deadline and r.start_date):
                continue
            if r.task_repeat == 'daily':
                print('dayly-----')
                data = r._prepare_task_data(date.today(), date.today() + (r.date_deadline - r.start_date))
                list_create.append(data)

            elif r.task_repeat == 'weekly':
                if (date.today() + timedelta(days=1)).weekday() == int(r.day_of_week):
                    data = r._prepare_task_data(date.today(), date.today() + (r.date_deadline - r.start_date))
                    list_create.append(data)  # xem read

            elif r.task_repeat == 'monthly':
                if r.day_of_month <= last_day:
                    if (date.today() + timedelta(days=1)).day == r.day_of_month:
                        data = r._prepare_task_data(date.today(), date.today() + (r.date_deadline - r.start_date))
                        list_create.append(data)
                else:
                    if (date.today() + timedelta(days=1)).day == last_day:
                        data = r._prepare_task_data(date.today(), date.today() + (r.date_deadline - r.start_date))
                        list_create.append(data)

        if list_create:
            self.env['project.task'].create(list_create)


    def _prepare_task_data(self, start_date, date_deadline):
        self.ensure_one()
        task_copy = self.copy({
            'name': self.name,
            'start_date': start_date,
            'date_deadline': date_deadline
        })
        return task_copy.read()