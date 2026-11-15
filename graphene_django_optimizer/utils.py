import graphql
from graphql import GraphQLSchema, GraphQLObjectType, FieldNode

noop = lambda *args, **kwargs: None


def is_iterable(obj):
    return hasattr(obj, "__iter__") and not isinstance(obj, str)


def get_field_def_compat(
    schema: GraphQLSchema, parent_type: GraphQLObjectType, field_node: FieldNode
):
    # graphql-core 3.3 removed graphql.execution.execute.get_field_def in favor of
    # GraphQLSchema.get_field, which also handles the introspection fields.
    if hasattr(schema, "get_field"):
        return schema.get_field(parent_type, field_node.name.value)

    from graphql.execution.execute import get_field_def

    return get_field_def(
        schema,
        parent_type,
        field_node.name.value if graphql.version_info < (3, 2) else field_node,
    )
