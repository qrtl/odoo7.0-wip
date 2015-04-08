# -*- coding: utf-8 -*-
#    Author: Joel Grand-Guillaume
#    Copyright 2013 Camptocamp SA
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

import logging
import xmlrpclib
from datetime import datetime, timedelta
import openerp.addons.decimal_precision as dp
from openerp.osv import fields, orm
from openerp.tools.translate import _
from openerp.addons.connector.connector import ConnectorUnit
from openerp.addons.connector.session import ConnectorSession
from openerp.addons.connector.exception import (NothingToDoJob,
                                                FailedJobError,
                                                IDMissingInBackend)
from openerp.addons.connector.queue.job import job
from openerp.addons.connector.unit.synchronizer import ExportSynchronizer
from openerp.addons.connector.unit.mapper import (mapping,
                                                  ImportMapper
                                                  )
from openerp.addons.connector_ecommerce.unit.sale_order_onchange import (
    SaleOrderOnChange)
from openerp.addons.connector_ecommerce.sale import (ShippingLineBuilder,
                                                     CashOnDeliveryLineBuilder,
                                                     GiftOrderLineBuilder)
# from .unit.backend_adapter import (GenericAdapter,
#                                    MAGENTO_DATETIME_FORMAT,
#                                    )
# from .unit.import_synchronizer import (DelayedBatchImport,
#                                        MagentoImportSynchronizer
#                                        )
# from .exception import OrderImportRuleRetry
# from .backend import magento
# from .connector import get_environment
# from .partner import PartnerImportMapper
from openerp.addons.magentoerpconnect.backend import magento
from openerp.addons.magentoerpconnect import sale

_logger = logging.getLogger(__name__)


@magento(replacing=sale.SaleOrderImportMapper)
class MySaleOrderImportMapper(sale.SaleOrderImportMapper):
    _model_name = 'magento.sale.order'
 
    @mapping
    def user_id(self, record):
        """ Assign the salesperson of the partner if any """
        session = self.session
        partner_rec = session.browse('res.partner', self.options.partner_id)
        if partner_rec.user_id:
            return {'user_id': partner_rec.user_id.id}
        return {'user_id': False}
