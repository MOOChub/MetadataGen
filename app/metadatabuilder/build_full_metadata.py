from app.metadatabuilder.build_organization import build_organization_fragment
from app.metadatabuilder.build_person import build_all_persons_fragments
from app.metadatabuilder.build_resource_type import build_resource_type_fragment
from app.metadatabuilder.build_optional_metadata import build_optional_metadata
from app.suggestion_logging.log_writer import write_log


def build_metadata(data: dict) -> dict:
    """
    Creates a metadata dictionary for a single course. It distinguishes between the mandatory
    attributes and the optional.

    :param data: The input metadata to be enriched and restructured to fit the MOOChub format.
    :type data: dict
    :return: A metadata dictionary conforming to the MOOChub metadata structure.
    :rtype: dict
    """
    publisher = build_organization_fragment(data["publisher"])
    creators = build_all_persons_fragments(data["creator"])

    metadata = {  # set of required attributes, minimum metadata according to MOOChub format
        "name": data["name"],
        "learningResourceType": build_resource_type_fragment(),
        "description": data["description"],  # Although it is not required by the MOOChub format, this program enforces
        # a description.
        "publisher": publisher,
        "creator": creators,
        "url": data["url"],
        "license": data["license"]
    }

    optional_attributes = build_optional_metadata(data)
    metadata.update(optional_attributes)

    try:
        write_log(metadata)
    except Exception as e:
        print(e)
        print("Problem with connecting to the suggestion log database...")
        print("Skipping logging the suggestions...")
        print("This has no effect on the metadata generation.")

    return metadata
