from Backend.Domain.TradingSystem.user_state import UserState
from Backend.Domain.TradingSystem.responsibility import Responsibility
from Backend.Domain.TradingSystem.store import Store
from Backend.response import Response, ParsableList
from Backend.Domain.TradingSystem.purchase_details import PurchaseDetails
from typing import List


class Member(UserState):

    def get_username(self):
        return Response(True, obj=self.username, msg="got username successfully")

    def __init__(self, user, username, responsibilities=None, purchase_details=[]):  # for DB initialization
        super().__init__(user)
        if responsibilities is None:
            responsibilities = dict()
        self.username = username
        self.responsibilities = responsibilities
        self.purchase_details = purchase_details
        # get cart data from DB

    def login(self, username, password):
        return Response(False, msg="Members cannot re-login")

    def register(self, username, password):
        return Response(False, msg="Members cannot re-register")

    def save_product_in_cart(self, store_id, product_id, quantity):
        response = super().save_product_in_cart(store_id, product_id, quantity)
        # update data in DB in later milestones
        return response

    def delete_from_cart(self, store_id, product_id):
        response = super().delete_from_cart(store_id, product_id)
        # update data in DB in later milestones
        return response

    def change_product_quantity(self, store_id, product_id, new_quantity):
        response = super().change_product_quantity(store_id, product_id, new_quantity)
        # update data in DB in later milestones
        return response

    def buy_cart(self, user, product_purchase_info):
        response = super().buy_cart(user, product_purchase_info)
        # update data in DB in later milestones
        return response

    def delete_products_after_purchase(self):
        response = super().delete_products_after_purchase()
        # update data in DB in later milestones
        self.purchase_details.append(response.object)
        return response

    def open_store(self, store_name):
        store = Store(store_name)
        self.responsibilities[store.get_id()] = Responsibility(self,
                                                               store)
        return Response[store](True, obj=store, msg="Store opened successfully")

    def get_purchase_history(self):
        return Response[List[PurchaseDetails]](True, obj=ParsableList(self.purchase_details), msg="Purchase history "
                                                                                                  "got successfully")

    def add_new_product(self, store_id, product_name, product_price, quantity):
        if store_id not in self.responsibilities:
            return Response(False, msg=f"this member do not own/manage store {store_id}")
        return self.responsibilities[store_id].add_product(product_name, product_price, quantity)

    def remove_product(self, store_id, product_id):
        if store_id not in self.responsibilities:
            return Response(False, msg=f"this member do not own/manage store {store_id}")
        return self.responsibilities[store_id].remove_product(product_id)

    def change_product_quantity_in_store(self, store_id, product_id, new_quantity):
        if store_id not in self.responsibilities:
            return Response(False, msg=f"this member do not own/manage store {store_id}")
        return self.responsibilities[store_id].change_product_quantity(product_id, new_quantity)

    def set_product_price(self, store_id, product_id,
                          new_price):
        if store_id not in self.responsibilities:
            return Response(False, msg=f"this member do not own/manage store {store_id}")
        return self.responsibilities[store_id].set_product_price(product_id, new_price)

    def appoint_new_store_owner(self, store_id, new_owner):
        if store_id not in self.responsibilities:
            return Response(False, msg=f"this member do not own/manage store {store_id}")
        return self.responsibilities[store_id].appoint_owner(new_owner)

    def appoint_new_store_manager(self, store_id, new_manager):
        if store_id not in self.responsibilities:
            return Response(False, msg=f"this member do not own/manage store {store_id}")
        return self.responsibilities[store_id].appoint_manager(new_manager)

    def add_manager_permission(self, store_id, username, permission):
        if store_id not in self.responsibilities:
            return Response(False, msg=f"this member do not own/manage store {store_id}")
        return self.responsibilities[store_id].add_manager_permission(username, permission)

    def remove_manager_permission(self, store_id, username, permission):
        if store_id not in self.responsibilities:
            return Response(False, msg=f"this member do not own/manage store {store_id}")
        return self.responsibilities[store_id].remove_manager_permission(username, permission)

    def dismiss_manager(self, store_id, manager):
        if store_id not in self.responsibilities:
            return Response(False, msg=f"this member do not own/manage store {store_id}")
        return self.responsibilities[store_id].remove_appointment(manager)

    def get_store_personnel_info(self, store_id):
        if store_id not in self.responsibilities:
            return Response(False, msg=f"this member do not own/manage store {store_id}")
        return self.responsibilities[store_id].get_store_appointments()

    def get_store_purchase_history(self, store_id):
        if store_id not in self.responsibilities:
            return Response(False, msg=f"this member do not own/manage store {store_id}")
        return self.responsibilities[store_id].get_store_purchases_history()

    def get_any_store_purchase_history(self, store_id):
        return Response(False, msg="Members cannot get any store's purchase history")

    def get_user_purchase_history(self, user_id):
        return Response(False, msg="Members cannot get any user's purchase history")