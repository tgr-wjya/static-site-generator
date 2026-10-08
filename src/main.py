import os
import shutil

from inline_markdown import extract_title, markdown_to_html_node


def copy_directory_contents(source_dir: str, destination_dir: str) -> None:
    if os.path.exists(destination_dir):
        shutil.rmtree(destination_dir)
    os.makedirs(destination_dir, exist_ok=True)

    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        destination_path = os.path.join(destination_dir, item)

        if os.path.isfile(source_path):
            shutil.copy(source_path, destination_path)
            print(f"Copied file: {source_path} -> {destination_path}")
        elif os.path.isdir(source_path):
            os.makedirs(destination_path, exist_ok=True)
            print(f"Created directory: {destination_path}")
            copy_directory_contents(source_path, destination_path)


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r", encoding="utf-8") as input_file:
        markdown = input_file.read()

    with open(template_path, "r", encoding="utf-8") as template_file:
        template = template_file.read()

    content_html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    generated = template.replace("{{ Title }}", title).replace(
        "{{ Content }}", content_html
    )

    destination_dir = os.path.dirname(dest_path)
    if destination_dir:
        os.makedirs(destination_dir, exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as output_file:
        output_file.write(generated)


def main() -> None:
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_dir = os.path.join(root_dir, "static")
    public_dir = os.path.join(root_dir, "public")

    if os.path.exists(static_dir):
        copy_directory_contents(static_dir, public_dir)
    else:
        print(f"Static directory not found: {static_dir}")

    generate_page(
        os.path.join(root_dir, "content", "index.md"),
        os.path.join(root_dir, "template.html"),
        os.path.join(public_dir, "index.html"),
    )


if __name__ == "__main__":
    main()
