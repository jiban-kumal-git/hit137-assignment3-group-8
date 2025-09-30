# Text displayed in the "OOP Notes" tab.

OOP_NOTES = """
OOP Concepts Demonstrated

1) Encapsulation
   - Model handlers store the Hugging Face pipeline in private attributes.
   - Access is provided through methods and properties.

2) Inheritance & Multiple Inheritance
   - Concrete handlers inherit from a shared abstract base class.
   - Mixins provide logging and error handling (multiple inheritance).

3) Polymorphism
   - All handlers implement a common process(input_data) interface.
   - The GUI calls the same method regardless of the concrete model.

4) Method Overriding
   - Subclasses override parent hooks such as _build_pipeline() and process().
   - Image handler customizes process() to accept file paths or PIL images.

5) Multiple Decorators
   - Stacked decorators log calls and measure runtime on key methods.
"""
