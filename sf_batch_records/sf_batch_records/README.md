# SF Batch Records

Electronic Batch Production Records (EBR) module for Odoo 18.

## Features

- Batch production records per campaign (product, output lot, quantity, production date).
- Consumed materials tracked with their lots and quantities.
- Executed steps with instructions and operators.
- Measured parameters with expected value, tolerance and in/out-of-specification status.
- Deviations (material, parameter, process, other) approved or rejected by QA.
- QA review and release workflow with reviewer/releaser signatures.
- Release blocked while out-of-spec parameters are not covered by an approved deviation (configurable).
- Multi-company support with record rules per company.
- QWeb PDF report: Batch Production Record.

## Configuration

In Settings &gt; Batch Records you can configure:

- Block release on out-of-spec parameters (enabled by default).

## Usage

1. Create a batch record (product, quantity, production date).
2. Add the consumed materials with their lots.
3. Document the steps and their operators.
4. Record the measured parameters; out-of-spec values are flagged automatically.
5. Declare a deviation for each out-of-spec parameter; QA approves or rejects it.
6. Submit the record for review, then release it (requires manager rights).
7. Print the batch record PDF from the form.

## Permissions

- `sf_batch_records.group_sf_batch_records_user` - day-to-day entry (records, materials, steps, parameters, deviations).
- `sf_batch_records.group_sf_batch_records_manager` - review, release, reject, cancellation and deviation approval.

## Support

For questions, bug reports or feature requests, contact tech5262@gmail.com.