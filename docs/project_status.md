1. CUSTOMER to ACCOUNT
M:N

One customer may hold several accounts, and one account may be shared by several customers.
Implementation: ACCOUNT_HOLDER connects CustomerID and AccountID. It also stores HolderSince and HolderType.


2. BRANCH to EMPLOYEE
1:N

One branch can employ many employees. Each employee is assigned to one branch.
Implementation: EMPLOYEE.BranchID references BRANCH.BranchID.


3. BRANCH to ACCOUNT
1:N

One branch can manage many accounts. Each account belongs to one branch in this design.
Implementation: ACCOUNT.BranchID references BRANCH.BranchID.


4. CUSTOMER to LOAN
1:N*

A customer can have multiple loans. Each loan record identifies one customer.
Implementation: LOAN.CustomerID references CUSTOMER.CustomerID.
*This follows the supplied schema, which provides a single CustomerID column in LOAN.


5. LOAN to LOAN_PAYMENT
1:N

One loan can have many repayments, while each payment belongs to one loan.
Implementation: LOAN_PAYMENT.LoanID references LOAN.LoanID.


6. ACCOUNT to5.66 TRANSACTION
1:N

One account can have many transaction records. Each transaction record refers to one account.
Implementation: TRANSACTION.AccountID references ACCOUNT.AccountID.