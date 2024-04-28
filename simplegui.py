import os
import tkinter as tk
from tkinter import messagebox
import sqlite3
import dmls
import report


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Python Hospital Management")

        self.menu_bar = tk.Menu(self)

        # Initialize menu
        self.init_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.init_menu.add_command(label="Database", command=self.create_database)
        self.init_menu.add_command(
            label="Data", command=self.load_data
        )  # Placeholder for Data
        self.init_menu.add_separator()
        self.init_menu.add_command(label="Exit", command=self.exit_program)
        self.menu_bar.add_cascade(label="Initialize", menu=self.init_menu)

        # Run menu
        self.run_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.run_menu.add_command(label="Report", command=self.open_query_window)
        self.menu_bar.add_cascade(label="Run", menu=self.run_menu)

        self.config(menu=self.menu_bar)

    def create_database(self):
        os.unlink("hospital.db")
        # Create SQLite3 database with a dummy table
        conn = sqlite3.connect("hospital.db")
        c = conn.cursor()
        ddls = [
            """
            create table if not exists wards (
              wid int,
              occupancy boolean,
              type varchar(10),
              constraint pk_wid primary key(wid)
            );
            """,
            """
                Create table if not exists nurses(
                  nnurse_id int,
                  nlicense_no varchar(20),
                  nname varchar(30),
                  ngender varchar(1),
                  ndept varchar(20),
                  ndob date,
                  shift varchar(1),
                  contact_no varchar(10),
                  years_of_experience int,
                  onduty boolean,
                  Constraint pk_nnurse_id primary key (nnurse_id)
                );
            """,
            """create table if not exists patients(
                      pid int,
                      pname varchar(50),
                      pgender char(1),
                      pdob date,
                      street varchar(30),
                      city varchar(20),
                      state varchar(50),
                      emergency_contact number(10),
                      blood_type varchar(5),
                      constraint pk_pid primary key(pid)
                );
                """,
            """
                 Create table if not exists assign_to (
                    wid int foreign_key references wards(wid),
                    nnurse_id int  references nurses(nnurse_id),
                    number_of_occupants int
                 );
                 """,
            """
                 Create table if not exists admitted_to (
                      pid int foreign_key references patients(pid),
                      wid int foreign_key references wards(wid),
                      admission_date date,
                      discharge_date date null
                    );
                 """,
            """
                    Create table if not exists doctors (
                      license_no varchar(20),
                      dname varchar(30),
                      ddob date,
                      dgender varchar(1),
                      specialisation varchar (20),
                      consulting_room_no int,
                      mobile_no varchar(10),
                      working_hours varchar(10),
                      dept varchar(20),
                      constraint pk_license_no primary key(license_no)
                    );
                 """,
            """
                 Create table if not exists medications (
                      mid int,
                      medname varchar (30),
                      manufacturer varchar(30),
                      dosage_form varchar(30),
                      age_limit int,
                      ingredients varchar(50),
                      expiry_date date,
                      cost_per_unit number,
                      side_effects varchar(50),
                      constraint pk_mid primary key(mid)

                    );
                 """,
            """
                    Create table if not exists prescriber (
                      license_no varchar foreign_key references doctors(license_no),
                      mid int foreign_key references medications(mid),
                      dosage varchar(20)
                    );
                 """,
            """
                 Create table if not exists tests (
                      tid int,
                      tname varchar(30),
                      ttype varchar(20),
                      cost number,
                      equipment varchar(30),
                      duration int,
                      lab_name varchar(30),
                      Constraint pk_tid primary key(tid)
                    );
                 """,
            """
            Create table test_result (
              test_date date,
              test_taken varchar(50),
              result varchar(100),
              test_id int,
              constraint fk_test_id foreign key(test_id) references tests
            );
            """,
            """
                 Create table if not exists performs (
                  license_no varchar foreign_key references doctors(license_no),
                  test
                );
                 """,
        ]

        for cmd in ddls:
            c.execute(cmd)
        conn.commit()
        conn.close()
        messagebox.showinfo(
            "Info", f"Database created successfully with {len(ddls)} tables."
        )

    def load_data(self):

        recs = 0

        conn = sqlite3.connect("hospital.db")
        c = conn.cursor()

        for nurse in dmls.nurses:
            recs += 1
            c.execute(nurse)

        for ward in dmls.wards:
            recs += 1
            c.execute(ward)

        for nw in dmls.nurse_to_ward:
            recs += 1
            c.execute(nw)

        for patient in dmls.patients:
            recs += 1
            c.execute(patient)

        for pw in dmls.patient_to_ward:
            recs += 1
            c.execute(pw)

        for doctor in dmls.doctors:
            recs += 1
            c.execute(doctor)

        for medicine in dmls.medicines:
            recs += 1
            c.execute(medicine)

        for test in dmls.medical_tests:
            recs += 1
            c.execute(test)

        for test_done in dmls.test_performed:
            recs += 1
            c.execute(test_done)

        for prescription in dmls.prescriptions:
            recs += 1
            c.execute(prescription)

        for aresult in dmls.test_results:
            recs += 1
            c.execute(aresult)

        conn.commit()
        conn.close()
        messagebox.showinfo("Info", f"Sample data inserted.  Total of {recs} rows.")

    def patient_in_wards(self):
        conn = sqlite3.connect("hospital.db")
        c = conn.cursor()

        c.execute(
            """
            select
              p.pname,
              w.type,
              a.admission_date,
              a.discharge_date
            from
              patients p
              join admitted_to a on p.pid = a.pid
              join wards w on a.wid = w.wid;
        """
        )
        rows = c.fetchall()
        conn.commit()
        conn.close()

        report.display_report(
            "Patient in Wards",
            ("Patient Name", "Ward", "Admitted On", "Discharged On"),
            rows,
        )

    def exit_program(self):
        self.destroy()

    def open_query_window(self):
        # Create a new window for query
        query_window = tk.Toplevel(self)
        query_window.title("Query Window")

        # Query buttons
        query1_btn = tk.Button(
            query_window, text="Patient in Wards", command=self.patient_in_wards
        )
        query1_btn.pack(padx=10, pady=10)

        query2_btn = tk.Button(
            query_window, text="Medicines Prescribed", command=self.medicines_prescribed
        )
        query2_btn.pack(padx=10, pady=10)

        query3_btn = tk.Button(
            query_window, text="Nurse Assignments", command=self.nurses_assignment
        )
        query3_btn.pack(padx=10, pady=10)

        query4_btn = tk.Button(
            query_window, text="Patient Age", command=self.patient_age
        )
        query4_btn.pack(padx=10, pady=10)

        query5_btn = tk.Button(
            query_window, text="Tests By Doctor", command=self.tests_by_doctor
        )
        query5_btn.pack(padx=10, pady=10)

        query6_btn = tk.Button(
            query_window, text="Average Age of Nurses", command=self.average_age
        )
        query6_btn.pack(padx=10, pady=10)

    def average_age(self):
        conn = sqlite3.connect("hospital.db")
        c = conn.cursor()

        c.execute(
            """
            select
              avg(years_of_experience) as average_experience
            from
              nurses;
        """
        )
        rows = c.fetchall()
        conn.close()
        messagebox.showinfo("Info", f"Average Age of nurses {rows[0][0]} years.", default="ok")

    def tests_by_doctor(self):
        conn = sqlite3.connect("hospital.db")
        c = conn.cursor()

        c.execute(
            """
            select
              d.dname as doctor_name,
              count(*) as test_count
            from
              performs p
              join doctors d on p.license_no = d.license_no
            group by
              d.dname;
        """
        )
        rows = c.fetchall()
        conn.commit()
        conn.close()

        report.display_report(
            "Tests Performed",
            ("Doctor", "Tests"),
            rows,
        )

    def patient_age(self):
        conn = sqlite3.connect("hospital.db")
        c = conn.cursor()

        c.execute(
            """
        select
          p.pname,
          strftime('%Y', 'now') - strftime('%Y', p.pdob) -
    (strftime('%m-%d', 'now') < strftime('%m-%d', p.pdob)) AS age
        from
          patients p
        """
        )
        rows = c.fetchall()
        conn.commit()
        conn.close()

        report.display_report(
            "Patients Age",
            (
                "Name",
                "Age",
            ),
            rows,
        )

    def nurses_assignment(self):
        conn = sqlite3.connect("hospital.db")
        c = conn.cursor()

        c.execute(
            """
            select
              n.nname as nurse_name,
              n.ngender as nurse_gender,
              n.years_of_experience as nurse_experience,
              n.onduty as nurse_on_duty,
              w.type as ward_type,
              w.occupancy as ward_occupied
            from
              nurses n
              join assign_to a on n.nnurse_id = a.nnurse_id
              join wards w on a.wid = w.wid
        """
        )
        rows = c.fetchall()
        conn.commit()
        conn.close()

        report.display_report(
            "Nurse Assignments",
            ("Name", "Gender", "Experience", "On duty", "ward", "Ward occupied"),
            rows,
        )

    def medicines_prescribed(self):
        conn = sqlite3.connect("hospital.db")
        c = conn.cursor()

        c.execute(
            """
        select
          d.dname,
          m.medname
        from
          doctors d
          join prescriber pr on d.license_no = pr.license_no
          join medications m on pr.mid = m.mid;
        """
        )
        rows = c.fetchall()
        conn.commit()
        conn.close()

        report.display_report(
            "Medicines prescribed",
            (
                "Doctor Name",
                "Medicine",
            ),
            rows,
        )


if __name__ == "__main__":
    app = App()
    app.mainloop()
