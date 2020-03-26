from fpdf import FPDF

class cvgen:
	def __init__(self, body, occ, employer, title):
		self.body = body
		self.occupation = occ
		self.employer = employer
		self.title = title

	def generate(self):

		modBody = self.body

		modBody = modBody.replace("XXX", self.occupation)
		modBody = modBody.replace("YYY", self.employer)

		pdf = FPDF()
		pdf.add_page()
		pdf.set_font("Arial", size=12)
		pdf.cell(200, 10, txt=modBody, ln=1, align="C")
		pdf.output(self.title)