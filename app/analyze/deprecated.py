"""
__authors__     = Yash, Will, Peter
__description__ = Deprecated version of doing text/speech analytics
__name__ = deprecated.py

__DEPRECATED__ = Do NOT use these funcions in main libraries
"""

API = { 
    'TA' : {'KEY':'ade69017-4581-4f52-a108-17f5955f0bef', 'PWD':'wrXmWscUqpmj'},
    'PI' : {'KEY':'4671c4a1-62f2-40ff-8cf4-e2791667a67b', 'PWD':'RinAFA18Jpmj'},
    'CS' : {'KEY':'07173885-f33f-4535-93dc-2b4965f256e8', 'PWD':'mo17ptJlJi2x'}
}

discovery = DiscoveryV1(
    username = API['CS']['KEY'],
    password = API['CS']['PWD'],
    version='2016-12-01'



def analyze_tone(text_array):
    tone_analyzer = ToneAnalyzerV3(
        username = API['TA']['KEY'],
        password = API['TA']['PWD'],
        version ='2016-05-19')

    tone_array = []
    for text in text_array:
        try:
            response = tone_analyzer.tone(text=text)
            tone = response['document_tone']['tone_categories'][0]['tones']
            tone_array.append(tone)
        except:
            tone_array.append('')

    return tone_array

def personalize(text_array):
    personality_insights = PersonalityInsightsV3(
        version = '2016-10-20',
        username = API['PI']['KEY'],
        password = API['PI']['PWD'])
    personality_array = []
    for profile_text in text_array:
        try:
            profile = personality_insights.profile(
                profile_text, content_type='text/plain',
                raw_scores=True, consumption_preferences=True)

            personality_array.append(profile)
        except:
            personality_array.append('')

    return personality_array

def clear_documents():
    result = cognitive_search({'return':'id'})

    while result['matching_results']:
        result = cognitive_search({'return':'id'})
        print('Deleting Old Records')
        for doc_id in result['results']:
            doc_id = doc_id['id']
            delete_doc = discovery.delete_document(
                '56eed52e-0538-4e43-92a8-a7223844e431', 
                'b5b60b1b-4e2b-4840-8bdc-da30a00f3e29', doc_id)

def write_to_discovery(text_array):
    env_id = '56eed52e-0538-4e43-92a8-a7223844e431'
    col_id = 'b5b60b1b-4e2b-4840-8bdc-da30a00f3e29'

    clear_documents()
    add_doc = None
    for i, text in enumerate(text_array):
        if text:
            document = Document()
            document.add_paragraph(text)
            fname = '{}/transcript'.format(s.TRANSCRIPT_DIR) + str(i) + '.docx'
            
            if os.path.isfile(fname):
                os.remove(fname)

            document.save(fname)
            with open(fname, 'rb') as outfile:    
                add_doc = discovery.add_document(env_id, col_id,
                                        file_info=outfile)
    if add_doc is None:
        return json.dumps('', indent=2)
    return json.dumps(add_doc, indent=2)

def cognitive_search(query_options):
    environments = discovery.get_environments()

    my_environments = [x for x in environments['environments'] if
                         x['name'] == 'byod']
    my_environment_id = my_environments[0]['environment_id']

    collections = discovery.list_collections(my_environment_id)
    my_collections = [x for x in collections['collections']]

    configurations = discovery.list_configurations(
        environment_id=my_environment_id)

    default_config_id = discovery.get_default_configuration_id(
        environment_id=my_environment_id)

    default_config = discovery.get_configuration(
        environment_id=my_environment_id, configuration_id=default_config_id)

    query_results = discovery.query(my_environment_id,
                                    my_collections[0]['collection_id'],
                                    query_options)
    
    return query_results


def deprecated_analyze(text_array):
    # DEPRECATED - use regular analyze function
    print('Analysing Tone...')
    tone_array = analyze_tone(text_array)
    print(tone_array)
    
    print('Building Personas...')
    personality_array = personalize(text_array)
    print(personality_array)
    
    print('Writing to Discovery')
    write_to_discovery(text_array)

    print('Performing Cognitive Search')
    entities = cognitive_search({'aggregation':'term(enriched_text.entities.text%2Ccount%3A5)'})
    concepts = cognitive_search({'aggregation':'term(enriched_text.concepts.text%2Ccount%3A5)'})

    concepts = concepts['aggregations'][0]['results']
    entities = entities['aggregations'][0]['results']

    keys = [entity['key'] for entity in entities]

    parties = find_parties(filename)
    print('Writing Results...')

    data = {}
    data['transcript'] = text_array
    data['tone'] = tone_array
    data['personality'] = personality_array
    data['keys'] = keys
    data['concepts']   = nlu_array["concepts"]
    data['parties']    = parties