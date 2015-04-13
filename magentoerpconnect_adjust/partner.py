# -*- coding: utf-8 -*-

# from openerp.osv import orm, fields
from openerp.addons.connector.unit.mapper import mapping
from openerp.addons.magentoerpconnect.backend import magento
from openerp.addons.magentoerpconnect.partner import PartnerImportMapper
# from openerp.addons.magentoerpconnect.partner import BaseAddressImportMapper
from openerp.addons.magentoerpconnect.partner import AddressImportMapper
# from .backend import magento_myversion



# @magento(replacing=PartnerImportMapper)
# class MyPartnerImportMapper(PartnerImportMapper):
#     _model_name = 'magento.res.partner'
@magento(replacing=AddressImportMapper)
class MyAddressImportMapper(AddressImportMapper):

    @mapping
    def property_account_position(self, record):
        if not record.get('region'):
            return
        state_ids = self.session.search('res.country.state',
                                        [('name', '=ilike', record['region'])])
#         if state_ids and state_ids[0].code != 'CA':
        if self.session.browse('res.country.state', state_ids)[0].code != 'CA':
            fp_ids = self.session.search('account.fiscal.position', [('name','=','Tax Exempt')])
            return {'property_account_position': fp_ids[0]}
        return

# #         fp_ids = self.session.search('account.fiscal.position', ['name','=','海外取引先'])
# #         return {'property_account_position': fp_ids[0]}
#         return {'property_account_position': 3}

