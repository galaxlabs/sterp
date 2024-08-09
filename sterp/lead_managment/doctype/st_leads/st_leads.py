# Copyright (c) 2024, SynchTech  and contributors
# For license information, please see license.txt
import frappe
from frappe.model.document import Document

class STLeads(Document):
    def on_update(self):
        self.create_or_update_crm_lead()

    def create_or_update_crm_lead(self):
        # Check if the lead already exists
        lead_exists = frappe.db.exists('Lead', {'lead_name': self.client_name})

        # Get primary and WhatsApp phone numbers
        primary_phone, whatsapp_phone = self.get_contact_phones()

        # Get primary email
        primary_email = self.get_contact_email()

        if lead_exists:
            # Update existing lead
            lead_doc = frappe.get_doc('Lead', {'lead_name': self.client_name})
            if primary_phone:
                lead_doc.phone = primary_phone
            if whatsapp_phone:
                lead_doc.whatsapp_no = whatsapp_phone  # Update WhatsApp number
            if primary_email:
                lead_doc.email_id = primary_email  # Update primary email
            lead_doc.save(ignore_permissions=True)
            frappe.msgprint(f'Lead {lead_doc.name} updated successfully!')
        else:
            # Create new lead
            lead_doc = frappe.get_doc({
                'doctype': 'Lead',
                'lead_name': self.client_name,
                'company_name': self.client_name,  # Assuming company name is same as client name
                'email_id': primary_email,  # Set primary contact email
                'phone': primary_phone,
                'whatsapp_no': whatsapp_phone,  # Set WhatsApp number
                'status': 'Lead',
                'lead_owner': self.owner  # Assuming the owner of the ST Lead is the lead owner
            })
            lead_doc.insert(ignore_permissions=True)
            frappe.msgprint(f'Lead {lead_doc.name} created successfully!')

    def get_contact_email(self):
        if self.contact_information:
            for contact in self.contact_information:
                if contact.is_primary:
                    return contact.email_id  # Use 'email_id' instead of 'email'
        return None

    def get_contact_phones(self):
        primary_phone = None
        whatsapp_phone = None
        if self.contact_nos:
            for contact in self.contact_nos:
                if contact.is_primary_mobile_no:
                    primary_phone = contact.phone
                if contact.custom_is_whatsapp:
                    whatsapp_phone = contact.phone
        return primary_phone, whatsapp_phone

# import frappe
# from frappe.model.document import Document

# class STLeads(Document):
#     def on_update(self):
#         self.create_or_update_crm_lead()

#     def create_or_update_crm_lead(self):
#         # Check if the lead already exists
#         lead_exists = frappe.db.exists('Lead', {'lead_name': self.client_name})

#         # Get primary and WhatsApp phone numbers
#         primary_phone, whatsapp_phone = self.get_contact_phones()

#         if lead_exists:
#             # Update existing lead
#             lead_doc = frappe.get_doc('Lead', {'lead_name': self.client_name})
#             if primary_phone:
#                 lead_doc.mobile_no = primary_phone  # Set primary phone number as mobile_no
#             if whatsapp_phone:
#                 lead_doc.whatsapp_no = whatsapp_phone  # Update WhatsApp number
#             lead_doc.save(ignore_permissions=True)
#             frappe.msgprint(f'Lead {lead_doc.name} updated successfully!')
#         else:
#             # Create new lead
#             lead_doc = frappe.get_doc({
#                 'doctype': 'Lead',
#                 'lead_name': self.client_name,
#                 'company_name': self.client_name,  # Assuming company name is same as client name
#                 'email_id': self.get_contact_email(),  # Assuming a method to get primary contact email
#                 'mobile_no': primary_phone,  # Set primary phone number as mobile_no
#                 'whatsapp_no': whatsapp_phone,  # Set WhatsApp number
#                 'status': 'Lead',
#                 'lead_owner': self.owner  # Assuming the owner of the ST Lead is the lead owner
#             })
#             lead_doc.insert(ignore_permissions=True)
#             frappe.msgprint(f'Lead {lead_doc.name} created successfully!')

#     def get_contact_email(self):
#         if self.contact_information:
#             for contact in self.contact_information:
#                 if contact.is_primary:
#                     return contact.email
#         return None

#     def get_contact_phones(self):
#         primary_phone = None
#         whatsapp_phone = None
#         if self.contact_nos:  # Updated to use contact_nos instead of contact_phone
#             for contact in self.contact_nos:
#                 if contact.is_primary_mobile_no:
#                     primary_phone = contact.phone
#                 if contact.custom_is_whatsapp:
#                     whatsapp_phone = contact.phone
#         return primary_phone, whatsapp_phone

# import frappe
# from frappe.model.document import Document

# class STLeads(Document):
#     def on_update(self):
#         self.create_or_update_crm_lead()

#     def create_or_update_crm_lead(self):
#         # Check if the lead already exists
#         lead_exists = frappe.db.exists('Lead', {'lead_name': self.client_name})

#         # Get primary and WhatsApp phone numbers
#         primary_phone, whatsapp_phone = self.get_contact_phones()

#         if lead_exists:
#             # Update existing lead
#             lead_doc = frappe.get_doc('Lead', {'lead_name': self.client_name})
#             if primary_phone:
#                 lead_doc.mobile_no = primary_phone  # Set primary phone number as mobile_no
#             if whatsapp_phone:
#                 lead_doc.whatsapp_no = whatsapp_phone  # Update WhatsApp number
#             lead_doc.save(ignore_permissions=True)
#             frappe.msgprint(f'Lead {lead_doc.name} updated successfully!')
#         else:
#             # Create new lead
#             lead_doc = frappe.get_doc({
#                 'doctype': 'Lead',
#                 'lead_name': self.client_name,
#                 'company_name': self.client_name,  # Assuming company name is same as client name
#                 'email_id': self.get_contact_email(),  # Assuming a method to get primary contact email
#                 'mobile_no': primary_phone,  # Set primary phone number as mobile_no
#                 'whatsapp_no': whatsapp_phone,  # Set WhatsApp number
#                 'status': 'Lead',
#                 'lead_owner': self.owner  # Assuming the owner of the ST Lead is the lead owner
#             })
#             lead_doc.insert(ignore_permissions=True)
#             frappe.msgprint(f'Lead {lead_doc.name} created successfully!')

#     def get_contact_email(self):
#         if self.contact_information:
#             for contact in self.contact_information:
#                 if contact.primary:
#                     return contact.email
#         return None

#     def get_contact_phones(self):
#         primary_phone = None
#         whatsapp_phone = None
#         if self.contact_phone:  # Ensure to access the contact_phone child table
#             for contact in self.contact_phone:
#                 if contact.is_primary_mobile_no:
#                     primary_phone = contact.phone
#                 if contact.custom_is_whatsapp:
#                     whatsapp_phone = contact.phone
#         return primary_phone, whatsapp_phone

# import frappe
# from frappe.model.document import Document

# class STLeads(Document):
#     def on_update(self):
#         self.create_or_update_crm_lead()

#     def create_or_update_crm_lead(self):
#         # Check if the lead already exists
#         lead_exists = frappe.db.exists('Lead', {'lead_name': self.client_name})

#         # Get primary and WhatsApp phone numbers
#         primary_phone, whatsapp_phone = self.get_contact_phones()

#         if lead_exists:
#             # Update existing lead
#             lead_doc = frappe.get_doc('Lead', {'lead_name': self.client_name})
#             if primary_phone:
#                 lead_doc.phone = primary_phone
#             if whatsapp_phone:
#                 lead_doc.whatsapp_no = whatsapp_phone  # Update WhatsApp number
#             lead_doc.save(ignore_permissions=True)
#             frappe.msgprint(f'Lead {lead_doc.name} updated successfully!')
#         else:
#             # Create new lead
#             lead_doc = frappe.get_doc({
#                 'doctype': 'Lead',
#                 'lead_name': self.client_name,
#                 'company_name': self.client_name,  # Assuming company name is same as client name
#                 'email_id': self.get_contact_email(),  # Assuming a method to get primary contact email
#                 'phone': primary_phone,
#                 'whatsapp_no': whatsapp_phone,  # Set WhatsApp number
#                 'status': 'Lead',
#                 'lead_owner': self.owner  # Assuming the owner of the ST Lead is the lead owner
#             })
#             lead_doc.insert(ignore_permissions=True)
#             frappe.msgprint(f'Lead {lead_doc.name} created successfully!')

#     def get_contact_email(self):
#         if self.contact_information:
#             for contact in self.contact_information:
#                 if contact.primary:
#                     return contact.email
#         return None

#     def get_contact_phones(self):
#         primary_phone = None
#         whatsapp_phone = None
#         if self.contact_information:
#             for contact in self.contact_information:
#                 if contact.primary:
#                     primary_phone = contact.phone
#                 if contact.is_whatsapp:
#                     whatsapp_phone = contact.phone
#         return primary_phone, whatsapp_phone


# import frappe
# from frappe.model.document import Document

# class STLeads(Document):
#     def on_update(self):
#         self.create_or_update_crm_lead()

#     def create_or_update_crm_lead(self):
#         # Check if the lead already exists
#         lead_exists = frappe.db.exists('Lead', {'lead_name': self.client_name})
#         primary_phone, whatsapp_phone = self.get_contact_phones()

#         if lead_exists:
#             # Update existing lead
#             lead_doc = frappe.get_doc('Lead', {'lead_name': self.client_name})
#             if primary_phone:
#                 lead_doc.phone = primary_phone
#             if whatsapp_phone:
#                 lead_doc.whatsapp_phone = whatsapp_phone
#             lead_doc.save(ignore_permissions=True)
#             frappe.msgprint(f'Lead {lead_doc.name} updated successfully!')
#         else:
#             # Create new lead
#             lead_doc = frappe.get_doc({
#                 'doctype': 'Lead',
#                 'lead_name': self.client_name,
#                 'company_name': self.client_name,  # Assuming company name is same as client name
#                 'email_id': self.get_contact_email(),  # Assuming a method to get primary contact email
#                 'phone': primary_phone,
#                 'whatsapp_phone': whatsapp_phone,
#                 'status': 'Lead',
#                 'lead_owner': self.owner  # Assuming the owner of the ST Lead is the lead owner
#             })
#             lead_doc.insert(ignore_permissions=True)
#             frappe.msgprint(f'Lead {lead_doc.name} created successfully!')

#     def get_contact_email(self):
#         if self.contact_information:
#             for contact in self.contact_information:
#                 if contact.primary:
#                     return contact.email
#         return None

#     def get_contact_phones(self):
#         primary_phone = None
#         whatsapp_phone = None
#         if self.contact_information:
#             for contact in self.contact_information:
#                 if contact.primary:
#                     primary_phone = contact.phone
#                 if contact.is_whatsapp:
#                     whatsapp_phone = contact.phone
#         return primary_phone, whatsapp_phone


# import frappe
# from frappe.model.document import Document

# class STLeads(Document):
#     def on_update(self):
#         self.create_crm_lead()

#     def create_crm_lead(self):
#         lead_exists = frappe.db.exists('Lead', {'lead_name': self.client_name})
#         if not lead_exists:
#             lead_doc = frappe.get_doc({
#                 'doctype': 'Lead',
#                 'lead_name': self.client_name,
#                 'company_name': self.client_name,  # Assuming company name is same as client name
#                 'email_id': self.get_contact_email(),  # Assuming a method to get primary contact email
#                 'phone': self.get_contact_phone(),  # Assuming a method to get primary contact phone
#                 'status': 'Lead',
#                 'lead_owner': self.owner  # Assuming the owner of the ST Lead is the lead owner
#             })
#             lead_doc.insert(ignore_permissions=True)
#             frappe.msgprint(f'Lead {lead_doc.name} created successfully!')

#     def get_contact_email(self):
#         if self.contact_information:
#             for contact in self.contact_information:
#                 if contact.primary:
#                     return contact.email
#         return None

#     def get_contact_phone(self):
#         if self.contact_nos:
#             for contact in self.contact_nos:
#                 if contact.primary:
#                     return contact.phone
#         return None
