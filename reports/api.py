from fastapi import FastAPI
from fastapi.responses import FileResponse
from fpdf import FPDF
import json
import requests
import logger

log = logger.getLogger("api")

## init ##
app = FastAPI()

## ## 
class PDF(FPDF):
    REPORT_FULLNAME = "/home/reports/todos.pdf"

    def header(self):
        self.set_font('Arial', 'B', 20)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 15, 'List of Todos', 1, 0, 'C',1)
        self.ln(30)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

    # Save document
    def save(self):
        self.output(self.REPORT_FULLNAME)
        log.info("Report stored in {0}.".format(self.REPORT_FULLNAME))
        return self.REPORT_FULLNAME

##
def _send_todos_request():
    resp = requests.get('http://xw-app-todos:5057/todos?showAll=true')
    if resp.status_code == 200:
        log.info("Received the list of todos from the xw-todos app. Status code: 200")
        return json.loads(resp.text)
    else: 
        log.error("Failed communication with the xw-todos app. Status code: {0}".format(resp.status_code))
        return "Error while saving Todo {0}".format(id)

def _create_report(todos):
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()

    pdf.add_font('DejaVu', '', '/home/reports/DejaVuSansCondensed.ttf', uni=True)
    pdf.set_font('DejaVu', '', 14)
    for todo in todos:
        if todo["isDone"]:
            pdf.cell(0, 10, "\u2611 {0} (id:{1})".format(todo["description"], todo["id"]), 0, 1)
        else:
            pdf.cell(0, 10, "\u2610 {0} (id:{1})".format(todo["description"], todo["id"]), 0, 1)

    log.debug("Report created. Number of todos: {0}.".format(len(todos)))
    return pdf.save()

## REST Endpoints ##
@app.get('/')
def hello():
    """Greetings"""
    return "So long and thanks for all the fish"

@app.get('/report', status_code=200)
def report():
    """Create a blank report"""
    log.debug("Request: GET '/report'")
    todos = _send_todos_request()
    report_path = _create_report(todos)
    log.debug("Report created and stored in {0}.".format(report_path))
    
    return FileResponse(report_path)
    