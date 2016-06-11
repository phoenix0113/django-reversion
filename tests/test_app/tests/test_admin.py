from django.contrib import admin
from django.shortcuts import resolve_url
import reversion
from reversion.admin import VersionAdmin
from test_app.models import TestModel, TestModelParent
from test_app.tests.base import LoginTestBase


class AdminTestBase(LoginTestBase):

    def setUp(self):
        super(AdminTestBase, self).setUp()
        reversion.unregister(TestModel)
        reversion.unregister(TestModelParent)
        admin.site.register(TestModelParent, VersionAdmin)

    def tearDown(self):
        super(AdminTestBase, self).tearDown()
        admin.site.unregister(TestModelParent)


class AdminRegisterTest(AdminTestBase):

    def setAutoRegister(self):
        self.assertTrue(reversion.is_registered(TestModelParent))

    def setAutoRegisterFollowsParent(self):
        self.assertTrue(reversion.is_registered(TestModel))


class AdminAddViewTest(AdminTestBase):

    def testAddView(self):
        self.client.post(resolve_url("admin:test_app_testmodelparent_add"), {
            "name": "v1",
            "parent_name": "parent_v1",
        })
        obj = TestModelParent.objects.get()
        self.assertSingleRevision((obj, obj.testmodel_ptr), user=self.user, comment="Added.")


class AdminUpdateViewTest(AdminTestBase):

    def testUpdateView(self):
        obj = TestModelParent.objects.create()
        self.client.post(resolve_url("admin:test_app_testmodelparent_change", obj.pk), {
            "name": "v2",
            "parent_name": "parent_v2",
        })
        self.assertSingleRevision((obj, obj.testmodel_ptr), user=self.user, comment="Changed name and parent_name.")


class AdminRevisionViewTest(AdminTestBase):

    def testRevisionView(self):
        with reversion.create_revision():
            obj = TestModelParent.objects.create()
        with reversion.create_revision():
            obj.name = "v2"
            obj.parent_name = "parent v2"
        response = self.client.get(resolve_url(
            "admin:test_app_testmodelparent_revision",
            obj.pk,
            reversion.get_for_object(obj)[1].pk,
        ))
        self.assertContains(response, 'value="v1"')
        self.assertContains(response, 'value="parent v1"')
        response = self.client.get(resolve_url(
            "admin:test_app_testmodelparent_revision",
            obj.pk,
            reversion.get_for_object(obj)[-].pk,
        ))
        self.assertContains(response, 'value="v2"')
        self.assertContains(response, 'value="parent v2"')
