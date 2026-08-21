{
    'name': 'Resource Capacity Planning',
    'version': '18.0.1.0',
    'category': 'Project',
    'summary': 'Allocate resources to projects, track capacity and avoid overload',
    'description': """
Resource Capacity Planning
==========================

Balance your team's workload across projects.

Key Features:
-------------
* Resource records: people or machines with daily capacity
* Resource allocation lines on project tasks and milestones
* Capacity vs allocation: utilization percentage computed live
* Overload warnings when a resource exceeds its capacity
* Filters by project, resource, team and period
* Per-resource and per-project dashboards
* Works with native project and task modules

Ideal for:
* Project managers balancing team workloads
* Service companies planning resource utilization
* Managers avoiding burnout and missed deadlines
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 149.75,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'project', 'hr', 'resource'],
    'data': [
        'security/resource_planning_security.xml',
        'security/ir.model.access.csv',
        'data/resource_planning_data.xml',
        'views/resource_planning_menus.xml',
        'views/resource_planning_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}