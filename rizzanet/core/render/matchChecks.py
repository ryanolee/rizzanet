
CHECKS = {
    'content/path': lambda node, content_path: node.get_path() == content_path,
    'content/id': lambda node, content_id: node.get_id() == content_id,
    'content_data/id': lambda node, content_data_id: node.get_content_data().get_id() == content_data_id,
    'content_data/type': lambda node, content_type_name: node.get_content_type().get_name() == content_type_name
}