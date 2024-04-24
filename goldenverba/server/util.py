from goldenverba.components.interfaces import Reader, Chunker, Embedder, Retriever, Generator
from goldenverba.verba_manager import VerbaManager

import json
import os

from wasabi import msg  # type: ignore[import]


def setup_managers(manager):
    msg.info("Setting up components")
    config = load_config(manager)
    set_config(manager, config)
    
def get_config(manager: VerbaManager, filename: str = "verba_config.json") -> dict:

    config = {}
    if os.path.exists(filename):
        with open(filename, "r") as file:
            config = json.load(file)

    setting_config = config.get("SETTING",{})

    available_environments = manager.environment_variables
    available_libraries = manager.installed_libraries

    readers = manager.reader_manager.get_readers()
    reader_config = {"components":{reader: readers[reader].get_meta(available_environments,available_libraries) for reader in readers}, "selected": manager.reader_manager.selected_reader}

    chunkers = manager.chunker_manager.get_chunkers()
    chunkers_config = {"components":{chunker: chunkers[chunker].get_meta(available_environments,available_libraries) for chunker in chunkers}, "selected": manager.chunker_manager.selected_chunker}

    embedders = manager.embedder_manager.get_embedders()
    embedder_config = {"components":{embedder: embedders[embedder].get_meta(available_environments,available_libraries) for embedder in embedders}, "selected": manager.embedder_manager.selected_embedder}

    retrievers = manager.retriever_manager.get_retrievers()
    retrievers_config = {"components":{retriever: retrievers[retriever].get_meta(available_environments,available_libraries) for retriever in retrievers}, "selected": manager.retriever_manager.selected_retriever}

    generators = manager.generator_manager.get_generators()
    generator_config = {"components":{generator: generators[generator].get_meta(available_environments,available_libraries) for generator in generators}, "selected": manager.generator_manager.selected_generator}

    return {"RAG": {"Reader": reader_config, "Chunker":chunkers_config, "Embedder":embedder_config, "Retriever":retrievers_config, "Generator": generator_config}, "SETTING":setting_config} 

def set_config(manager: VerbaManager, combined_config: dict):

    save_config(combined_config)
    config = combined_config.get("RAG", {})

    # Set Selected
    manager.reader_manager.set_reader(config.get("Reader",{}).get("selected",""))
    manager.chunker_manager.set_chunker(config.get("Chunker",{}).get("selected",""))
    manager.embedder_manager.set_embedder(config.get("Embedder",{}).get("selected",""))
    manager.retriever_manager.set_retriever(config.get("Retriever",{}).get("selected",""))
    manager.generator_manager.set_generator(config.get("Generator",{}).get("selected",""))

    # Set Config
    readers = manager.reader_manager.get_readers()
    for _reader in config.get("Reader",{}).get("components",{}):
        if _reader in readers:
            readers[_reader].set_config(config.get("Reader",{}).get("components",{}).get(_reader,{}).get("config",{}))

    chunkers = manager.chunker_manager.get_chunkers()
    for _chunker in config.get("Chunker",{}).get("components",{}):
        if _chunker in chunkers:
            chunkers[_chunker].set_config(config.get("Chunker",{}).get("components",{}).get(_chunker,{}).get("config",{}))

    embedders = manager.embedder_manager.get_embedders()
    for _embedder in config.get("Embedder",{}).get("components",{}):
        if _embedder in embedders:
            embedders[_embedder].set_config(config.get("Embedder",{}).get("components",{}).get(_chunker,{}).get("config",{}))

    retrievers = manager.retriever_manager.get_retrievers()
    for _retriever in config.get("Retriever",{}).get("components",{}):
        if _retriever in retrievers:
            retrievers[_retriever].set_config(config.get("Retriever",{}).get("components",{}).get(_chunker,{}).get("config",{}))

    generators = manager.generator_manager.get_generators()
    for _generator in config.get("Generator",{}).get("components",{}):
        if _generator in generators:
            generators[_generator].set_config(config.get("Generator",{}).get("components",{}).get(_chunker,{}).get("config",{}))

def save_config(config: dict, filename: str = "verba_config.json"):
    """Save config to file."""
    with open(filename, "w") as file:
        msg.good("Saved Config")
        json.dump(config, file, indent=4)

def load_config(manager, filename: str = "verba_config.json"):
    """Save config to file."""
    msg.good("Saved Config")
    if os.path.exists(filename):
        with open(filename, "r") as file:
            config = json.load(file)
            return config
    else:
        return get_config(manager)

