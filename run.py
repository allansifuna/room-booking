from bookingapp import create_app
app = create_app()

from add_admin import init_db
import click

@app.cli.command()
def set_db():
    """Add Adminstartor"""

    click.echo("----Initializing the database----")
    init_db()
    click.echo("----Done!----")

if __name__ == '__main__':
    app.run(debug=True)
