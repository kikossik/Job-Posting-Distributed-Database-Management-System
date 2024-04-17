# class JobRouter:
#     """
#     A router to control all database operations on models in the Job application.
#     """
#     EAST_COAST_STATES = {'CT', 'DE', 'FL', 'GA', 'ME', 'MD', 'MA', 'NH', 'NJ', 'NY', 'NC', 'PA', 'RI', 'SC', 'VA', 'VT', 'WV'}
#     WEST_COAST_STATES = {'CA', 'OR', 'WA', 'AK', 'HI'}
#     MID_STATES = {'AL', 'AZ', 'AR', 'CO', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'MN', 'MS', 'MO', 'MT', 'MI', 'NE', 'NV', 'NM', 'ND', 'OH', 'OK', 'SD', 'TN', 'TX', 'UT', 'WI', 'WY'}

#     def db_for_read(self, model, **hints):
#         """
#         Attempts to read Job models go to the appropriate database.
#         """
#         if model._meta.model_name == 'job':
#             state_code = hints.get('instance', None).state_code if hints.get('instance') else None
#             if state_code in EAST_COAST_STATES:
#                 return 'east_coast_db'
#             elif state_code in WEST_COAST_STATES:
#                 return 'west_coast_db'
#             elif state_code in MID_STATES:
#                 return 'mid_states_db'
#         return None

#     def db_for_write(self, model, **hints):
#         """
#         Attempts to write Job models go to the appropriate database.
#         """
#         return self.db_for_read(model, **hints)

#     def allow_relation(self, obj1, obj2, **hints):
#         """
#         Allow relations if a model in the Job app is involved.
#         """
#         if obj1._meta.app_label == 'job' or obj2._meta.app_label == 'job':
#             return True
#         return None

#     def allow_migrate(self, db, app_label, model_name=None, **hints):
#         """
#         Make sure the Job app only appears in the 'job_db'
#         """
#         if app_label == 'job':
#             return db in ['east_coast_db', 'west_coast_db', 'mid_states_db']
#         return None
