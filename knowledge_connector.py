def create_knowledge_base(project_id, display_name):
    """Creates a Knowledge base.

    Args:
        project_id: The GCP project linked with the agent.
        display_name: The display name of the Knowledge base."""
    from google.cloud import dialogflow_v2beta1 as dialogflow
    client = dialogflow.KnowledgeBasesClient()
    project_path = client.common_project_path(project_id)

    knowledge_base = dialogflow.KnowledgeBase(
        display_name=display_name)

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

def detect_intent_knowledge(project_id, session_id, language_code,
                            knowledge_base_id, texts):
    """Returns the result of detect intent with querying Knowledge Connector.

    Args:
    project_id: The GCP project linked with the agent you are going to query.
    session_id: Id of the session, using the same `session_id` between requests
              allows continuation of the conversation.
    language_code: Language of the queries.
    knowledge_base_id: The Knowledge base's id to query against.
    texts: A list of text queries to send.
    """
    from google.cloud import dialogflow_v2beta1 as dialogflow
    session_client = dialogflow.SessionsClient()

    session_path = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session_path))

    for text in texts:
        text_input = dialogflow.TextInput(
            text=text, language_code=language_code)

        query_input = dialogflow.QueryInput(text=text_input)

        knowledge_base_path = dialogflow.KnowledgeBasesClient \
            .knowledge_base_path(project_id, knowledge_base_id)

        query_params = dialogflow.QueryParameters(
            knowledge_base_names=[knowledge_base_path])

        request = dialogflow.DetectIntentRequest(
            session=session_path,
            query_input=query_input,
            query_params=query_params
        )
        response = session_client.detect_intent(request=request)

        print('=' * 20)
        print('Query text: {}'.format(response.query_result.query_text))
        print('Detected intent: {} (confidence: {})\n'.format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence))
        print('Fulfillment text: {}\n'.format(
            response.query_result.fulfillment_text))
        print('Knowledge results:')
        knowledge_answers = response.query_result.knowledge_answers
        for answers in knowledge_answers.answers:
            print(' - Answer: {}'.format(answers.answer))
            print(' - Confidence: {}'.format(
                answers.match_confidence))
