# cvgen testing (not for deployment)

import cvgen

# Generate file
cv = cvgen.cvgen("Hello, I want to apply for XXX position with YYY", "A JOB", "Mayfield Inc", "file.pdf")
cv.generate()