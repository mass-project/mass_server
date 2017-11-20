from mongoengine import Q


class GraphFunctions:
    @staticmethod
    def get_relation_graph(sample, depth=3):
        current_depth = 0
        samples_at_current_depth = [sample.id]
        all_queried_samples = []
        found_relations = set()

        while current_depth < depth:
            from mass_server.core.models import SampleRelation
            relations_at_current_depth = SampleRelation.objects(Q(sample__in=samples_at_current_depth) | Q(other__in=samples_at_current_depth)).no_dereference()
            all_queried_samples.extend(samples_at_current_depth)
            samples_at_next_depth = []
            for relation in relations_at_current_depth:
                found_relations.add(relation)
                if relation.sample.id not in all_queried_samples:
                    samples_at_next_depth.append(relation.sample.id)
                if relation.other.id not in all_queried_samples:
                    samples_at_next_depth.append(relation.other.id)
            samples_at_current_depth = samples_at_next_depth
            current_depth += 1
        return found_relations
