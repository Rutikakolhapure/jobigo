# E2E Smoke Test Plan

This file lists a minimal set of end-to-end smoke tests you can run manually or automate with a tool like Playwright or Cypress.

1) Authentication + Job browsing
   - Sign up a new seeker user
   - Login and obtain access token
   - Visit Jobs page and open a published job

2) Apply flow
   - From job detail, click 'Apply' (or use API) to create an application
   - Verify application appears under /applications

3) Saved jobs
   - Save a job from job detail
   - Verify it appears under /saved-jobs

4) Chat
   - Open chat (authenticated) and send a message
   - Confirm message appears for another client (open a second browser/incognito)

5) AI Job Matcher
   - Paste resume text and run matcher
   - Confirm results include job IDs linking to job detail

Automating these tests is recommended using Playwright or Cypress; let me know if you want me to add Playwright scaffolding and a basic script.
