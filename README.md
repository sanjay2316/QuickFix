### Quickfix

Mobile Repair Shop

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch quickfix
bench install-app quickfix
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/quickfix
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade
### CI

This app can use GitHub Actions for CI. The following workflows are configured:

- CI: Installs this app and runs unit tests on every push to `develop` branch.
- Linters: Runs [Frappe Semgrep Rules](https://github.com/frappe/semgrep-rules) and [pip-audit](https://pypi.org/project/pip-audit/) on every pull request.


### License

mit

### Answer
1)def validate(self):
    self.total = sum(r.amount for r in self.items)
    self.save()
    other = frappe.get_doc("Spare Part", self.part)
    other.stock_qty -= self.qty
    other.save()

Answer : 1)You should not use save() method inside a validate because it will lead to recursion error
          2)You can save object of another doc in validate 
          

2)why would you see a "Document has been modified after you have opened it" error, and how does Frappe prevent concurrent overwrites? (One paragraph.)

Answer : 2)To avoid the concurrent change in a same field at the same time and to make the record as Data Integrity

3)rename a test Technician record. Does assigned_technician on linked Job Cards update automatically? Why or why not?

Answer : 3) it will not change because it is already saved

4)why is frappe.get_all dangerous in a whitelisted method exposed to low-privilege users?

Answer : 4) frappe.get_all is consider to be dangerous because whitelist method is exposed outside and when we use get_all it ignore's the user permissions so that anyone can access the records

5)Call self.save() inside on_update and observe what breaks so happens?

Answer : 5)on_update has default property to save so when we use save again inside on_update it made into recursion pitfall

6)why does a frappe.call inside the validate client event not work, and why must async fetches happen in onload/refresh instead?

Answer : 6) validate is synchronous method while the frappe.call will take time and it is asynchronous instead of waiting it saves . Onload / Refresh will wait as async.

7) explain the difference between putting a frappe.get_all() call directly inside the Jinja template versus pre-computing in before_print() and referencing doc.precomputed_field.

Answer : 7) before_print hook will call a precompute method where the doc.precomputed_field like print summary so that it avoid unwanted call repeatedly.

8)The snippet below has an N+1 query problem. Identify it and rewrite it:
N+1 PROBLEM 
job_cards = frappe.get_all("Job Card", fields=["name","assigned_technician"])
for jc in job_cards:
    tech = frappe.get_doc("Technician", jc.assigned_technician)
    print(tech.technician_name, tech.phone)

Answer : 8)


9)show the f-string version side by side with the parameterized version, and explain why the latter is always preferred.

Answer : 9) when we use the f-string version the data is injected inside the query i makes sql injection so the parameterized is safer

10)Add a JS field hide that hides customer_phone for non-managers on the Job Card form — then show that a direct API call can still retrieve the field. Explain in README_internals.md why hiding a field in JavaScript is not a security measure.

Answer : 10)js is not directly linked with the backend so the the js will hide only in form like frontend . If you want to hide in api also then use perm level through field settings . 
