from ..base import APITest

URL = '/v1/claims/'


class ClaimListPostGeneralSuccessTest(APITest):
    pass

# TODO
#    def test_should_set_location_header(self):
#        pass

# TODO
#    def test_should_set_user_provided_data(self):
#        pass

# TODO
#    def test_should_set_automatic_fields(self):
#        pass


class ClaimListPostSuccessWithoutContentionTest(APITest):
    def setUp(self):
        super(ClaimListPostSuccessWithoutContentionTest, self).setUp()
        self.post_data = {
            'resource': 'post-resource',
            'timeout': 0.010,
        }
        self.response = self.client.post(URL, data=self.post_data)

    def test_should_return_201(self):
        self.assertEqual(201, self.response.status_code)

# TODO
#    def test_should_set_status_to_active(self):
#        pass

# TODO
#    def test_should_set_ttl_to_timeout(self):
#        pass


class ClaimListPostSuccessWithContentionTest(APITest):
    pass

# TODO
#    def test_should_return_202(self):
#        pass

# TODO
#    def test_should_set_status_to_waiting(self):
#        pass

class ClaimListPostErrorTest(APITest):
    def test_missing_mandatory_parameters_should_return_400(self):
        no_params_response = self.client.post(URL, data={})
        self.assertEqual(400, no_params_response.status_code)
        self.assertIn('resource', no_params_response.data)
        self.assertIn('timeout', no_params_response.data)

        no_resource_response = self.client.post(URL, data={
            'timeout': 1.2,
        })
        self.assertEqual(400, no_resource_response.status_code)
        self.assertIn('resource', no_resource_response.data)

        no_timeout_response = self.client.post(URL, data={
            'resource': 'foo',
        })
        self.assertEqual(400, no_timeout_response.status_code)
        self.assertIn('timeout', no_timeout_response.data)

# TODO
#    def test_invalid_parameter_values_should_return_400(self):
#        pass

# TODO
#    def test_unknown_parameters_should_return_400(self):
#        pass