def create_knowledge_base(project_id, display_name):
    """Creates a Knowledge base.

    Args:
        project_id: The GCP project linked with the agent.
        display_name: The display name of the Knowledge base."""
#     from google.cloud import dialogflow_v2beta1 as dialogflow
    client = dialogflow_v2beta1.KnowledgeBasesClient(credentials = credentials)
    project_path = client.project_path(project_id)

    knowledge_base = dialogflow_v2beta1.types.KnowledgeBase(display_name=display_name)

    response = client.create_knowledge_base(
        parent=project_path,
        knowledge_base=knowledge_base
    )

    print('Knowledge Base created:\n')
    print('Display Name: {}\n'.format(response.display_name))
    print('Knowledge ID: {}\n'.format(response.name))
    
def create_document(project_id, knowledge_base_id, display_name, mime_type,
                    knowledge_type, content_uri):
    """Creates a Document.

    Args:
        project_id: The GCP project linked with the agent.
        knowledge_base_id: Id of the Knowledge base.
        display_name: The display name of the Document.
        mime_type: The mime_type of the Document. e.g. text/csv, text/html,
            text/plain, text/pdf etc.
        knowledge_type: The Knowledge type of the Document. e.g. FAQ,
            EXTRACTIVE_QA.
        content_uri: Uri of the document, e.g. gs://path/mydoc.csv,
            http://mypage.com/faq.html."""
    from google.cloud import dialogflow_v2beta1 as dialogflow
    client = dialogflow.DocumentsClient()
    knowledge_base_path = dialogflow.KnowledgeBasesClient.knowledge_base_path(
        project_id, knowledge_base_id)

    document = dialogflow.Document(
        display_name=display_name, mime_type=mime_type,
        content_uri=content_uri)

    document.knowledge_types.append(
        getattr(dialogflow.Document.KnowledgeType, knowledge_type)
    )

    response = client.create_document(parent=knowledge_base_path, document=document)
    print('Waiting for results...')
    document = response.result(timeout=120)
    print('Created Document:')
    print(' - Display Name: {}'.format(document.display_name))
    print(' - Knowledge ID: {}'.format(document.name))
    print(' - MIME Type: {}'.format(document.mime_type))
    print(' - Knowledge Types:')
    for knowledge_type in document.knowledge_types:
        print('    - {}'.format(KNOWLEDGE_TYPES[knowledge_type]))
    print(' - Source: {}\n'.format(document.content_uri))

def detect_intent_knowledge(
    project_id,
    session_id,
    language_code,
    knowledge_base_id,
    texts
):
    """Returns the result of detect intent with querying Knowledge Connector.

    Args:
    project_id: The GCP project linked with the agent you are going to query.
    session_id: Id of the session, using the same `session_id` between requests
              allows continuation of the conversation.
    language_code: Language of the queries.
    knowledge_base_id: The Knowledge base's id to query against.
    texts: A list of text queries to send.
    """
    credentials = service_account.Credentials.from_service_account_file(service_account_file)
    session_client = dialogflow_v2beta1.SessionsClient(credentials=credentials)
    session_path = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session_path))
    response_list = []
    for text in texts:
        text_input = dialogflow_v2beta1.types.TextInput(
            text=text,
            language_code="en"
        )    
        query_input = dialogflow_v2beta1.types.QueryInput(
            text=text_input
        )
        knowledge_base_path = dialogflow_v2beta1.KnowledgeBasesClient.knowledge_base_path(
            project_id,
            knowledge_base_id
        )
        query_params = dialogflow_v2beta1.types.QueryParameters(
            knowledge_base_names=[knowledge_base_path]
        )
        response = session_client.detect_intent(
            session=session_path,
            query_input=query_input,
            query_params=query_params
        )
        
        response_list.append(response)

    return response_list
