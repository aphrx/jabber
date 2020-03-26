from fpdf import FPDF

class cvgen:
	def __init__(self, body, occ, employer, loc, title):
		self.body = body
		self.occupation = occ
		self.employer = employer
		self.location = loc
		self.title = title



	def generate(self):

		modBody = self.body

		modBody = modBody.replace("XXX", self.occupation)
		modBody = modBody.replace("YYY", self.employer)
		modBody = modBody.replace("ZZZ", self.location)
		modBody = modBody.replace("  ", "\n")

		pdf = FPDF()
		pdf.add_page()
		pdf.set_font("Arial", size=11)
		pdf.multi_cell(0, 6, txt=modBody, align="L")
		pdf.output(self.title)