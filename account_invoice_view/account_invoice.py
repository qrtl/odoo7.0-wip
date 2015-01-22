# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) Rooms For (Hong Kong) Limited T/A OSCG. All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv
from datetime import datetime
from tools.translate import _
import openerp.addons.decimal_precision as dp

class account_invoice(osv.osv):
    _inherit = 'account.invoice'
    
    def _get_inv_base_amt(self, cr, uid, ids, field_names, args, context=None):
        res = {}
        for invoice in self.browse(cr, uid, ids, context=context):
            # set the rate 1.0 if the transaction currency is the same as the base currency
            if invoice.company_id.currency_id == invoice.currency_id:
                rate = 1.0
            else:
                if invoice.date_invoice:
                    invoice_date_datetime = datetime.strptime(invoice.date_invoice, '%Y-%m-%d')
                else:
                    today = context.get('date', datetime.today().strftime('%Y-%m-%d'))
                    invoice_date_datetime = datetime.strptime(today, '%Y-%m-%d')

                rate_obj = self.pool['res.currency.rate']
                rate_rec = rate_obj.search(cr, uid, [
                    ('currency_id', '=', invoice.currency_id.id),
                    ('name', '<=', invoice_date_datetime),
                    # not sure for what purpose 'currency_rate_type_id' field exists in the table, but keep this line just in case
                    ('currency_rate_type_id', '=', None)
                    ], order='name desc', limit=1, context=context)
                if rate_rec:
                    rate = rate_obj.read(cr, uid, rate_rec[0], ['rate'], context=context)['rate']
                else:
                    rate = 1.0
            res[invoice.id] = {
                'rate': rate,
                'residual_base': invoice.residual / rate,
                'amount_total_base': invoice.amount_total / rate,
                }
        return res

    _columns ={
               'rate': fields.function(_get_inv_base_amt, type='float', string=u'Rate', multi='base_amt'),
               'residual_base': fields.function(_get_inv_base_amt, type='float', digits_compute=dp.get_precision('Account'), string=u'Balance (Base)', multi="base_amt"),
               'amount_total_base': fields.function(_get_inv_base_amt, type='float', digits_compute=dp.get_precision('Account'), string=u'Total (Base)', multi="base_amt"),
               }

account_invoice()
