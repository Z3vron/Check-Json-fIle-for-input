import sys
import json
import unittest

def verify_input_json(json_file):
    try:
        data = json.loads(json_file)    
        if "PolicyDocument" not in data or "Statement" not in data["PolicyDocument"]:
            print("Missing components in the Json file.")
            return True
        
        for statement in data["PolicyDocument"]["Statement"]:
            if not isinstance(statement, dict):
                print("Statement should be a dictionary.")
                return True
            if "Resource" in statement:
                if statement["Resource"] == "*":
                    return False
        return True
            
    except FileNotFoundError:
        print("Given file couldn't be found.")
        return False
    
    except json.JSONDecodeError:
        print("Invalid JSON format.")
        return False
    
class test_verify_input_json(unittest.TestCase):
    
    def test_valid_json(self):
        json_data = '''
        {
            "PolicyDocument": {
                "Statement": [
                    {
                        "Resource": "arn:aws:s3:::example-bucket",
                        "Effect": "Allow",
                        "Action": "s3:GetObject"
                    }
                ]
            }
        }
        '''
        self.assertTrue(verify_input_json(json_data))
    
    def test_missing_policy_document_key(self):
        json_data = '{"Statement": []}'
        self.assertTrue(verify_input_json(json_data))
    
    def test_invalid_policy_document_value(self):
        json_data = '{"PolicyDocument": "not_a_dict", "Statement": []}'
        self.assertTrue(verify_input_json(json_data))
    
    def test_missing_statement_key(self):
        json_data = '{"PolicyDocument": {}}'
        self.assertTrue(verify_input_json(json_data))
    
    def test_invalid_statement_value(self):
        json_data = '{"PolicyDocument": {"Statement": "not_a_list"}}'
        self.assertTrue(verify_input_json(json_data))
    
    def test_invalid_resource_value(self):
        json_data = '''
        {
            "PolicyDocument": {
                "Statement": [
                    {
                        "Resource": 123
                    }
                ]
            }
        }
        '''
        self.assertTrue(verify_input_json(json_data))
    
    def test_correct_resource_value(self):
        json_data = '''
        {
            "PolicyName": "root",
            "PolicyDocument": {
                "Version": "2012-10-17",
                "Statement": [{
                    "Sid": "IamListAccess",
                    "Effect": "Allow",
                    "Action": [
                        "iam:ListRoles",
                        "iam:ListUsers"
                    ],
                    "Resource": "*"
                }]
            }
        }
        '''
        self.assertFalse(verify_input_json(json_data))

def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--run_unit_tests":
        unittest.main(argv=sys.argv[:1])
    elif len(sys.argv) == 2:
        input_file = sys.argv[1]
        with open(input_file, 'r') as file:
            input_file = file.read()
        verification = verify_input_json(input_file)
        print("Result of verification of given Json file:", verification)

if __name__ == '__main__':
    main()

