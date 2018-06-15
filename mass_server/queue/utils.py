import json

import mass_server.queue.queue_context as queue_context
from mass_server.api.schemas import AnalysisRequestSchema, SampleSchema


def enqueue_analysis_request(request):
    message_body = {
        'analysis_request': AnalysisRequestSchema().dump(request),
        'sample': SampleSchema().dump(request.sample)
    }

    queue_name = '{}_analysis-requests'.format(request.analysis_system.identifier_name)
    queue_context.channel.basic_publish(exchange='',
                                        routing_key=queue_name,
                                        body=json.dumps(message_body))
    request.enqueued = True
    request.save()
    print('enqueued {}'.format(request))
