---
applyTo: "src/tjbots/app/**"
---

## Structure 

- This is a Shiny for Python app. Do not confuse this for Shiny for R.
- Main entrypoint is in app.py. 
- From the entrypoint, there will be calls out to modules in `modules/` and components in `components/`. 
    - Modules are useful for a general purpose application and contain logic. 
    - Components are focused on the parts of the app and should contain little logic. 

## Testing 

- There are a few levels of tests:
    1. Unit testing of individual components
    2. Integration testing of individual modules or components 
    3. End-to-end testing of the entire application
    4. Docker testing of the built application package
- For testing levels 2, 3, and 4, we use the standard Shiny testing framework utilising Playwright. Refer to [the documentation](https://shiny.posit.co/py/docs/end-to-end-testing.html) for how to implement this appropriately.