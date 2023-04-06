#### 
# This file contains all the mappings provided
# mappings map the user provided strings (pre-defined)
# to specific faker module functions.
#####

from .custom_callbacks import random_choice, sequential_choice, sequence
from faker import Faker


fake = Faker()


varchar = {
	'name':fake.name,
	'first_name':fake.first_name,
	'last_name':fake.last_name,
	'address':fake.address,
	'male_name':fake.name_male,
	'female_name':fake.name_female,
	'job':fake.job,
	'phone_number':fake.phone_number,
	'email':fake.email,
	'md5':fake.md5,
	'sha1':fake.sha1,
	'uuid':fake.uuid4,
	'date_of_birth':fake.date_of_birth
}

date_time = {
	'future_datetime':fake.future_datetime,
	'past_datetime':fake.past_datetime,
	'future_date':fake.future_date,
	'past_date':fake.past_date,
	'time':fake.time,
	'date':fake.date,
	'unix_time':fake.unix_time
}


# generate pure random numbers for entropy
numbers = {
	'random_int':fake.random_int,
	'random_digit':fake.random_int,
	'sequence':sequence()
}


custom = {
	'random_choice':random_choice,
	'sequential_choice':sequential_choice()
}


# global mappings
mapping = {
	**numbers,
	**varchar,
	**date_time,
	**custom
}