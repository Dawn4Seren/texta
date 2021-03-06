from .settings import preprocessor_map
from utils.helper_functions import add_dicts

PREPROCESSOR_INSTANCES = {
    preprocessor_code: preprocessor['class'](**preprocessor['arguments'])
    for preprocessor_code, preprocessor in preprocessor_map.items() if preprocessor['is_enabled']
}


class DocumentPreprocessor(object):
    """A static document preprocessor adapter that dispatches the preprocessing request to appropriate preprocessor implementations.
    """

    @staticmethod
    def process(documents, **kwargs):
        """Dispatches the preprocessing request for the provided documents to the provided preprocessors.

        SIDE EFFECT: alters the documents in place.

        :param documents: collection of key-value documents, which are to be preprocessed
        :param kwargs[preprocessors]: document enhancing entities, which add new features to the existing documents
        :param kwargs: request parameters which must include entries for the preprocessors to work appropriately
        :type documents: list of dicts
        :type kwargs[preprocessors]: list of preprocessor implementation instances.
        :return: enhanced documents
        :rtype: list of dicts
        """
        preprocessors = kwargs['preprocessors']
        # Add metadata from all preprocessors
        processed_documents = {}
        if preprocessors:
            for preprocessor_code in preprocessors:
                preprocessor = PREPROCESSOR_INSTANCES[preprocessor_code]
                batch_documents = preprocessor.transform(batch_documents, **kwargs)
                add_dicts(processed_documents, batch_documents)
                documents = batch_documents['documents']

        else:
            processed_documents['documents'] = documents
        return processed_documents
