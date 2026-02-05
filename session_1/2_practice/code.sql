-- Enable readable output format
.mode columns
.headers on

-- Instructions for students:
-- 1. Open SQLite in terminal: sqlite3 library.db
-- 2. Load this script: .read code.sql
-- 3. Exit SQLite: .exit


-- write your sql code here

--(1) List all loans (title,member,date)
-- select title,name,loan_date from Loans
-- inner join Books on Loans.book_id=Books.id
-- inner join Members on Loans.member_id=Members.id;

--(2) List all books and any associated loans
-- select title,name,loan_date from Books
-- left join Loans on Books.id=Loans.book_id
-- left join Members on Loans.member_id=Members.id;

--(3) List all library branches and books held
-- select name,title from LibraryBranch
-- left join Books on LibraryBranch.id=Books.branch_id;

--(4) List each branch and book count
-- select name,count(title) as book_count from LibraryBranch
-- left join Books on LibraryBranch.id=Books.branch_id
-- group by LibraryBranch.id;

--(5) List each branch that holds more than 7 books
-- select name,count(title) as book_count from LibraryBranch
-- left join Books on LibraryBranch.id=Books.branch_id
-- group by LibraryBranch.id
-- having book_count>7;

--(6) List each member and the number of loans they have
-- select name,count(loan_date) as loan_count from Members
-- left join Loans on Members.id=Loans.member_id
-- group by member_id;

--(7) List each member who has never loaned a book
-- select name from Members
-- left join Loans on Members.id=Loans.member_id
-- group by member_id
-- having count(loan_date)=0;

--(8) For each branch show total loans
-- select name,count(loan_date) as total_loans from LibraryBranch
-- left join Books on LibraryBranch.id=Books.branch_id
-- left join Loans on Books.id=Loans.book_id
-- group by LibraryBranch.id;

--(9) List members with an active loan
-- select name from Members
-- inner join Loans on Members.id=Loans.member_id
-- where return_date is null;

--(10) Show all books and all loans with a column for loan status
select title,name,
case
    when return_date is null and loan_date is not null then 'Loaned book'
    else 'Unloaned book'
end as loan_status
from Books
left join Loans on Books.id=Loans.book_id
left join Members on Loans.member_id=Members.id;