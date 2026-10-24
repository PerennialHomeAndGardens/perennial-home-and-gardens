# Required garden-gift collection — prepared, not live

The owner's corrected requirements are implemented on this staging branch:
- Homepage gift section and first popup require name and valid email.
- The first offer and gift confirmation do not mention the newsletter.
- Gift access unlocks only after the collection endpoint acknowledges the request; rejected or failed submissions preserve the entered details and keep access closed.
- The second advertisement separately requests Perennial Garden Magazine signup. Gift requests are explicitly classified as gifts only, not newsletter subscriptions.
- Existing contact/service draft handling, artwork, tools, audio and navigation are retained.

## Receiving service
Account-free FormSubmit endpoint: https://formsubmit.co/ajax/perennialhomeandgardens@gmail.com . This is a form-to-email relay, not a mailing-list automation platform. It requires receiving-address confirmation before forwarding submissions. No new account or paid service was created.

## Blocker
Automatic approval review rejected the attempted setup request because the owner had not explicitly authorized sending Perennial's email address and administrative setup data to FormSubmit. No activation request is confirmed. Do not retry that setup request or activate this branch on the live site without the owner's explicit authorization for that destination.

The connected Gmail account is Examine the Past, not the receiving Perennial inbox, so a confirmation link delivered to Perennial's inbox cannot be read here through the present Gmail connection.

## Next step
Obtain permission to send the one-time setup request to FormSubmit using perennialhomeandgardens@gmail.com. Then confirm the receiving address through its inbox, submit a clearly marked test, and verify actual capture/delivery before publishing. Do not describe the list as collecting visitor addresses until that end-to-end check succeeds.

## Tests
The browser workflow intercepts every FormSubmit request. It checks required fields, gift/newsletter separation, success/failure handling, timed article prompts and responsive widths without sending email. Its passing result would establish interface behavior only, not live delivery or activation.
