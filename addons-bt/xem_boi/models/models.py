# -*- coding: utf-8 -*-
from datetime import date

import requests
from bs4 import BeautifulSoup
from dateutil import tz

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CustomPartner(models.Model):
    _inherit = 'res.partner'

    birthday = fields.Datetime(groups='xem_boi.group_warlock')
    date_of_birth = fields.Char(compute='_compute_all', compute_sudo=True)
    time_of_birth = fields.Char(compute='_compute_all', compute_sudo=True, groups='xem_boi.group_warlock')
    age = fields.Integer(compute='_compute_all', compute_sudo=True)
    manager_id = fields.Many2one('res.users', string='Manager')
    business_type = fields.Char(string='Business Type', compute='_compute_business')
    business = fields.Text(string='Business', compute='_compute_business')

    # 3002226135
    @api.depends('vat')
    def _compute_business(self):
        for r in self:
            if r.vat:
                result = r._crawl_data(r.vat)
                r.business = str(result['business'])
                r.business_type = result['business_type']
            else:
                r.business = ''
                r.business_type = ''

    @api.depends('birthday')
    def _compute_all(self):
        str_tz = self.env.context['tz']
        for r in self:
            if r.birthday:
                r.age = self.calculate_age(r.birthday)
                r.date_of_birth = self.convert_time(r.birthday, str_tz).strftime('%d/%m')
                r.time_of_birth = self.convert_time(r.birthday, str_tz).strftime('%H:%M')
            else:
                r.age = False
                r.date_of_birth = False
                r.time_of_birth = False

    def convert_time(self, datetime, str_tz):
        to_zone = tz.gettz(str_tz)
        result = datetime.astimezone(to_zone)
        return result

    def calculate_age(self, birthDate):
        today = date.today()
        age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
        print(today, birthDate)
        return age

    def _crawl_data(self, tax_code):
        response = requests.post("https://masothue.com/Ajax/Search", data={'q': tax_code})
        data = response.json()
        if 'url' in data:
            url = f"https://masothue.com{data['url']}"
        else:
            return {'business':'', 'business_type': ''}

        response = requests.get(url)
        data_html = BeautifulSoup(response.content, 'html.parser')
        result = {'business_type': data_html.find(class_='fa fa-building').parent.nextSibling.a.contents[0]}
        businesses = ''
        table_tr = data_html.find_all(class_='table')[0].tbody.find_all('tr')
        for item in table_tr:
            table_tds = item.find_all('td')
            businesses += table_tds[1].text + "||"

        result['business'] = businesses.split('||')
        return result
