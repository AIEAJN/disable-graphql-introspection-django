from django.test import TestCase
from graphene_django.utils.testing import GraphQLTestCase
from django.urls import reverse
from .models import AppConfig

class URLTests(TestCase):
    def test_graphql_url(self):
        # Data initialization
        AppConfig.objects.create(allow_introspection=True)
        self.assertTrue(AppConfig.objects.filter(allow_introspection=True).exists())
        response = self.client.get(reverse('graphql'))
        self.assertEqual(response.status_code, 400)
        

class QueryTests(GraphQLTestCase):
    def test_greeting(self):
        # Data initialization
        AppConfig.objects.create(allow_introspection=True)
        self.assertTrue(AppConfig.objects.filter(allow_introspection=True).exists())
        response = self.query(
            '''
            query{
                greeting
            }
            ''',
        )
        self.assertEqual(response.status_code, 200)
        content = response.json()
        self.assertResponseNoErrors(response)
        self.assertEqual(content['data']['greeting'], 'Hello World')
        
    def test_introspection_active(self):
        # Data initialization
        AppConfig.objects.create(allow_introspection=True)
        self.assertTrue(AppConfig.objects.filter(allow_introspection=True).exists())
        response = self.query(
            '''
            query {
                __schema {
                    types {
                        name
                    }
                }
            }
            ''',
        )
        content = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIn('__schema', content['data'])
    
    def test_introspection_innactive(self):
        # Data initialization
        AppConfig.objects.create(allow_introspection=False)
        self.assertTrue(AppConfig.objects.filter(allow_introspection=False).exists())
        response = self.query(
            '''
            query {
                __schema {
                    types {
                        name
                    }
                }
            }
            ''',
        )
        content = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(content['message'], 'Introspection is not allowed!')
    

class MutationTests(GraphQLTestCase):
    def test_update_introspection_status_to_true(self):
        # Data initialization
        AppConfig.objects.create(allow_introspection=False)
        self.assertTrue(AppConfig.objects.filter(allow_introspection=False).exists())
        response = self.query(
            """
            mutation{
                updateConfig(allowIntrospection: true){
                    success
                    message
                    allowIntrospection
                }
            }
            """
        )
        self.assertEqual(response.status_code, 200)
        content = response.json()
        self.assertTrue(content['data']['updateConfig']['success'])
        self.assertEqual(content['data']['updateConfig']['message'], 'success')
        self.assertTrue(content['data']['updateConfig']['allowIntrospection'])
        
    def test_update_introspection_status_to_false(self):
        # Data initialization
        AppConfig.objects.create(allow_introspection=True)
        self.assertTrue(AppConfig.objects.filter(allow_introspection=True).exists())
        response = self.query(
            """
            mutation{
                updateConfig(allowIntrospection: false){
                    success
                    message
                    allowIntrospection
                }
            }
            """
        )
        self.assertEqual(response.status_code, 200)
        content = response.json()
        self.assertTrue(content['data']['updateConfig']['success'])
        self.assertEqual(content['data']['updateConfig']['message'], 'success')
        self.assertFalse(content['data']['updateConfig']['allowIntrospection'])