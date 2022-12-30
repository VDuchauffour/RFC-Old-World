from Core import *
from Types import *
	

def in_area(string, area):
	if area is not None:
		return text("TXT_KEY_VICTORY_IN_AREA", string, AREA.format(area))
	return string


def outside_area(string, area):
	if area is not None:
		return text("TXT_KEY_VICTORY_OUTSIDE_AREA", string, AREA.format(area))
	return string


def religion_adjective(string, iReligion):
	if iReligion is not None:
		return text("TXT_KEY_VICTORY_RELIGION_ADJECTIVE", string, RELIGION_ADJECTIVE.format(iReligion))
	return string
	

def with_religion_in_cities(string, iReligion):
	if iReligion is not None:
		return text("TXT_KEY_VICTORY_WITH_RELIGION_IN_CITIES", string, RELIGION.format(iReligion))
	return string


class Progress(object):
		
	def format(self, requirements, evaluator):
		list_progress = self.format_list(requirements, evaluator)
		item_progress = self.format_items(requirements, evaluator)
		
		return list(list_progress) + list(item_progress)
		
	def format_list(self, requirements, evaluator):
		for requirement in requirements:
			progress = requirement.progress(evaluator)
			if isinstance(progress, list):
				for row in progress:
					yield row
	
	def format_items(self, requirements, evaluator):
		item_progress = self.get_item_progress(requirements, evaluator)
		row_size = self.get_row_size(item_progress)
		
		for index in range(0, len(item_progress), row_size):
			yield " ".join(progress for progress in item_progress[index:index+row_size])
		
	def get_item_progress(self, requirements, evaluator):
		item_progress = [requirement.progress(evaluator) for requirement in requirements]
		return [progress for progress in item_progress if not isinstance(progress, list)]
	
	def get_row_size(self, items):
		if len(items) % 4 == 0:
			return 4
		elif len(items) % 3 == 0:
			return 3
		elif len(items) % 4 > len(items) % 3:
			return 4
		else:
			return 3


class Description(object):

	def format(self, requirements, desc_args, global_suffixes, required=None):
		grouped_descriptions = self.grouped_descriptions(requirements)
		description_entries = [self.format_entry(key, typed_parameters, descriptions, desc_args + list(req_args), suffixes, required) for key, typed_parameters, req_args, descriptions, suffixes in grouped_descriptions]
		
		description = format_separators(description_entries, ",", text("TXT_KEY_AND"))
		
		return " ".join([description] + list(global_suffixes))
	
	def grouped_descriptions(self, requirements):
		arguments = self.arguments(requirements)
		
		grouped_descriptions = appenddict()
		for key, typed_parameters, desc_args, description, suffixes in arguments:
			grouped_descriptions[(key, typed_parameters, desc_args, suffixes)].append(description)
		
		for key, typed_parameters, desc_args, _, suffixes in arguments:
			if (key, typed_parameters, desc_args, suffixes) in grouped_descriptions:
				yield (key, typed_parameters, desc_args, grouped_descriptions.pop((key, typed_parameters, desc_args, suffixes)), suffixes)
	
	def arguments(self, requirements):
		return [(req_key, tuple(zip(req.GLOBAL_TYPES, self.convert_parameters(req.parameters))), tuple(req_args), req.description(), tuple(req_suffixes)) for req, req_key, req_args, req_suffixes in requirements]
	
	def convert_parameters(self, parameters):
		for parameter in parameters:
			if isinstance(parameter, list):
				parameter = tuple(parameter)
			yield parameter
	
	def format_entry(self, key, typed_parameters, descriptions, desc_args, suffixes, required):
		descriptions = format_separators(descriptions, ",", text("TXT_KEY_AND"))
		parameters = [type.format(parameter) for type, parameter in typed_parameters]
		
		if required is not None:
			descriptions = text("TXT_KEY_VICTORY_REQUIRED_OUT_OF", COUNT.format(required), descriptions)
		
		combined_desc_args = [descriptions] + desc_args + parameters
		return " ".join([text(key, *combined_desc_args)] + list(suffixes))


PROGRESS = Progress()
DESCRIPTION = Description()

