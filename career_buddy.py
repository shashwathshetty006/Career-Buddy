import tkinter as tk
from tkinter import ttk, messagebox  # Imported messagebox for error reporting
def suggest_careers(form_data):
    # 1. Extract and clean data safely
    education = form_data.get('education', '').lower()
    prev_field = form_data.get('previous_field', '').lower()
    tech_skills = form_data.get('technical_skills', '').lower()
    soft_skills = form_data.get('soft_skills', '').lower()
    experience = form_data.get('experience', '')
    domains = form_data.get('domains', [])  # Expecting a list

    motivation = form_data.get('motivation', '').lower()
    personality = form_data.get('personality', '').lower()
    long_term = form_data.get('long_term_goal', '').lower()

    work_env = form_data.get('work_environment', '').lower()
    salary = form_data.get('desired_salary', '')
    strengths = form_data.get('strengths', '').lower()

    suggestions = []

    # 2. LOGIC MATCHING

    # --- EDUCATION ---
    if any(x in education for x in ['phd', 'doctorate', 'post doc', 'master', 'm.tech', 'ms', 'mba']):
        suggestions += ["Research Scientist", "University Lecturer", "Senior Consultant"]

    if any(x in education for x in
           ['bachelor', 'diploma', 'high school', 'b.tech', 'b.e', 'bsc', 'degree', 'undergrad']):
        # Tech branch
        if any(x in tech_skills for x in ['coding', 'programming', 'python', 'java', 'c++', 'html', 'sql', 'data']):
            suggestions += ["Software Developer", "Data Analyst", "Web Developer"]

        # Finance branch
        if any(x in prev_field for x in ['finance', 'account', 'banking', 'commerce', 'economics']):
            suggestions.append("Financial Analyst")

        # Design branch
        if any(x in prev_field for x in ['design', 'art']) or 'photoshop' in tech_skills or 'figma' in tech_skills:
            suggestions.append("Graphic Designer")

        # Healthcare branch
        if any(x in prev_field for x in ['bio', 'health', 'medical', 'pharma']):
            suggestions.append("Healthcare Administrator")

    # --- EXPERIENCE ---
    exp_map = {'0': 0, '1-2': 2, '3-5': 4, '6-10': 8, '10+': 12}
    exp_years = exp_map.get(experience, 0)

    if exp_years >= 5:
        suggestions += ["Senior Specialist", "Management Consultant"]

    # --- PERSONALITY & STRENGTHS ---
    if any(x in personality for x in ['creative', 'artistic', 'imaginative']):
        suggestions += ["Content Creator", "Digital Marketer", "UX Designer"]

    if any(x in personality for x in ['analytical', 'logical', 'detail']) or 'problem solving' in strengths:
        suggestions += ["Business Analyst", "Data Scientist", "Quality Assurance Engineer"]

    if any(x in personality for x in ['extrovert', 'outgoing', 'social']) and 'communication' in soft_skills:
        suggestions += ["Public Relations Manager", "Sales Manager", "HR Specialist"]

    if 'introvert' in personality or 'research' in strengths:
        suggestions.append("Research Analyst")

    # --- GOALS ---
    if any(x in long_term for x in ['manager', 'lead', 'director', 'vp']):
        suggestions += ["Project Manager", "Team Lead"]

    if any(x in long_term for x in ['startup', 'business', 'own company', 'entrepreneur']):
        suggestions.append("Entrepreneur / Founder")

    # --- DOMAINS ---
    domain_map = {
        'technology': ["IT Consultant", "Network Administrator", "Systems Engineer"],
        'business & finance': ["Accountant", "Financial Planner", "Investment Banker"],
        'healthcare': ["Medical Researcher", "Health Informatics Specialist"],
        'arts & design': ["UX/UI Designer", "Illustrator", "Art Director"],
        'entrepreneurship': ["Business Developer", "Product Manager"]
    }

    for d in domains:
        key = d.lower()
        if key in domain_map:
            suggestions += domain_map[key]

    # --- WORK ENV & SALARY ---
    if 'remote' in work_env:
        suggestions += ["Freelance Developer", "Remote Content Writer"]

    if salary == 'high':
        domains_str = " ".join(domains).lower()
        if 'technology' in domains_str:
            suggestions.append("Machine Learning Engineer")
        if 'business' in domains_str or 'finance' in domains_str:
            suggestions.append("Investment Banker")

    suggestions = list(dict.fromkeys(suggestions))

    if not suggestions:
        suggestions = ["General Consultant", "Freelancer", "Office Administrator", "Career Counselor"]

    return suggestions


# GUI APPLICATION
class CareerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Career Suggestion App")
        self.root.geometry("600x750")

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TLabel', font=('Segoe UI', 10))
        self.style.configure('TButton', font=('Segoe UI', 10, 'bold'), background='#007bff', foreground='white')
        self.style.configure('Header.TLabel', font=('Segoe UI', 16, 'bold'), foreground='#333')

        # --- Scrollable Container ---
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=1)

        self.canvas = tk.Canvas(self.main_frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.inner_frame = tk.Frame(self.canvas, padx=20, pady=20)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.inner_frame, text="Career Path Finder", style='Header.TLabel').pack(pady=(0, 20))

        def add_label(text):
            ttk.Label(self.inner_frame, text=text).pack(anchor='w', pady=(10, 2))

        # --- FORM FIELDS ---
        add_label("Age Group")
        self.age_var = tk.StringVar(value="18–25")
        ttk.Combobox(self.inner_frame, textvariable=self.age_var, state="readonly",
                     values=["Below 18", "18–25", "26–35", "36–45", "45+"]).pack(fill='x')

        add_label("Education (e.g., B.Tech, MBA, High School)")
        self.edu_entry = ttk.Entry(self.inner_frame)
        self.edu_entry.pack(fill='x')

        add_label("Previous Field (e.g., Finance, IT, Sales)")
        self.prev_field_entry = ttk.Entry(self.inner_frame)
        self.prev_field_entry.pack(fill='x')

        add_label("Technical Skills (e.g., Python, Excel, Design)")
        self.tech_skills_entry = ttk.Entry(self.inner_frame)
        self.tech_skills_entry.pack(fill='x')

        add_label("Soft Skills (e.g., Communication, Leadership)")
        self.soft_skills_entry = ttk.Entry(self.inner_frame)
        self.soft_skills_entry.pack(fill='x')

        add_label("Experience Level")
        self.exp_var = tk.StringVar(value="0")
        ttk.Combobox(self.inner_frame, textvariable=self.exp_var, state="readonly",
                     values=["0", "1-2", "3-5", "6-10", "10+"]).pack(fill='x')

        add_label("Domains of Interest (Select at least one)")
        self.domain_vars = {}
        domains = ["Technology", "Business & Finance", "Healthcare", "Arts & Design", "Entrepreneurship"]
        for domain in domains:
            var = tk.BooleanVar()
            ttk.Checkbutton(self.inner_frame, text=domain, variable=var).pack(anchor='w')
            self.domain_vars[domain] = var

        add_label("Motivation")
        self.motivation_entry = tk.Text(self.inner_frame, height=3, font=('Segoe UI', 9))
        self.motivation_entry.pack(fill='x')

        add_label("Personality (e.g., Creative, Logical, Introvert)")
        self.personality_entry = ttk.Entry(self.inner_frame)
        self.personality_entry.pack(fill='x')

        add_label("Long Term Goal (e.g., Manager, Business Owner)")
        self.lt_goal_entry = ttk.Entry(self.inner_frame)
        self.lt_goal_entry.pack(fill='x')

        add_label("Preferred Work Environment")
        self.env_var = tk.StringVar(value="office")
        ttk.Combobox(self.inner_frame, textvariable=self.env_var, state="readonly",
                     values=["remote", "office", "hybrid"]).pack(fill='x')

        add_label("Desired Salary")
        self.salary_var = tk.StringVar(value="medium")
        ttk.Combobox(self.inner_frame, textvariable=self.salary_var, state="readonly",
                     values=["any", "low", "medium", "high"]).pack(fill='x')

        add_label("Key Strengths")
        self.strengths_entry = ttk.Entry(self.inner_frame)
        self.strengths_entry.pack(fill='x')

        # SUBMIT BUTTON
        submit_btn = ttk.Button(self.inner_frame, text="Generate Recommendations", command=self.on_submit)
        submit_btn.pack(pady=30, ipady=5, fill='x')

        # Initial canvas update
        self.inner_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def on_submit(self):
        try:
            # 1. Gather data
            selected_domains = [name for name, var in self.domain_vars.items() if var.get()]

            form_data = {
                'education': self.edu_entry.get(),
                'previous_field': self.prev_field_entry.get(),
                'technical_skills': self.tech_skills_entry.get(),
                'soft_skills': self.soft_skills_entry.get(),
                'experience': self.exp_var.get(),
                'domains': selected_domains,
                'motivation': self.motivation_entry.get("1.0", tk.END).strip(),
                'personality': self.personality_entry.get(),
                'long_term_goal': self.lt_goal_entry.get(),
                'work_environment': self.env_var.get(),
                'desired_salary': self.salary_var.get(),
                'strengths': self.strengths_entry.get()
            }

            # 2. Get results
            results = suggest_careers(form_data)

            # 3. Show Results
            self.show_results_window(results)

        except Exception as e:
            # THIS IS KEY: If anything crashes, you will see it here
            messagebox.showerror("Execution Error", f"An error occurred while generating results:\n{e}")
            print(f"Error: {e}")  # Also print to console

    def show_results_window(self, careers):
        result_win = tk.Toplevel(self.root)
        result_win.title("Your Recommendations")
        result_win.geometry("450x550")
        result_win.configure(bg="#f0f2f5")

        # Ensure window is on top and focused
        result_win.lift()
        result_win.focus_force()
        result_win.grab_set()

        tk.Label(result_win, text="Recommended Careers", font=('Segoe UI', 14, 'bold'), bg="#f0f2f5", fg="#333").pack(
            pady=15)

        list_frame = tk.Frame(result_win, bg="#f0f2f5")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)

        text_widget = tk.Text(list_frame, wrap=tk.WORD, bg="white", height=15, relief=tk.FLAT, font=('Segoe UI', 11))
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scroll = ttk.Scrollbar(list_frame, command=text_widget.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.config(yscrollcommand=scroll.set)

        if not careers:
            text_widget.insert(tk.END, "No specific matches found. Try entering keywords like 'Python' or 'Creative'!",
                               'default')
        else:
            text_widget.insert(tk.END, "Based on your profile:\n\n", 'header')
            for career in careers:
                text_widget.insert(tk.END, f"• {career}\n", 'bullet')

            text_widget.tag_configure('header', font=('Segoe UI', 10, 'italic'), foreground='gray')
            text_widget.tag_configure('bullet', font=('Segoe UI', 11, 'bold'), foreground='#007bff', spacing1=5,
                                      spacing3=5)

        text_widget.config(state=tk.DISABLED)

        ttk.Button(result_win, text="Close", command=result_win.destroy).pack(pady=15)
        self.root.wait_window(result_win)


if __name__ == "__main__":
    root = tk.Tk()
    app = CareerApp(root)
    root.mainloop()