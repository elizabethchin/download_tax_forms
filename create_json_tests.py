import unittest
import create_json



class TestCreateJSON(unittest.TestCase):

    def test_create_json(self):

        self.assertEqual(create_json.create_json("Form W-2"), 
        {'form_number': 'Form W-2', 'form_title': 'Wage and Tax Statement (Info Copy Only)', 'min_year': 1954.0, 'max_year': 2021.0})
        
        self.assertEqual(create_json.create_json(""), None)




    def test_list_of_tax_form_objects(self):

        self.assertEqual(create_json.list_of_tax_form_objects(["Form W-2", "Form 11-C", "Form 1095-C"]),
        [{'form_number': 'Form W-2', 'form_title': 'Wage and Tax Statement (Info Copy Only)', 'min_year': 1954.0, 'max_year': 2021.0}, {'form_number': 'Form 11-C', 'form_title': 'Occupational Tax and Registration Return for Wagering', 'min_year': 1974.0, 'max_year': 2017.0}, {'form_number': 'Form 1095-C', 'form_title': 'Employer-Provided Health Insurance Offer and Coverage', 'min_year': 2014.0, 'max_year': 2021.0}])

        self.assertEqual(create_json.list_of_tax_form_objects(""), None)

        self.assertEqual(create_json.list_of_tax_form_objects("form W-2"), None)

        self.assertEqual(create_json.list_of_tax_form_objects(["form W-2"]), 
        [{'form_number': 'Form W-2', 'form_title': 'Wage and Tax Statement (Info Copy Only)', 'min_year': 1954.0, 'max_year': 2021.0}])

        self.assertEqual(create_json.list_of_tax_form_objects([" form  W-2"]), 
        [{'form_number': 'Form W-2', 'form_title': 'Wage and Tax Statement (Info Copy Only)', 'min_year': 1954.0, 'max_year': 2021.0}])

        self.assertEqual(create_json.list_of_tax_form_objects("formW-2"), None)

    

if __name__ == '__main__':
    unittest.main()