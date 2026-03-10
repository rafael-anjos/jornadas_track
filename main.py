import sys
import os

def _base_dir() -> str:
    if getattr(sys, "frozen", False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


BASE = _base_dir()
sys.path.insert(0, os.path.join(BASE, "src"))

from controller.dashboard_controller import DashboardController
from view.main_view import MainView
from view.dashboard_view import DashboardView
from view.jornadas_view import JornadasView
from view.infracoes_view import InfracoesView


if __name__ == "__main__":
    main_view = MainView()

    dashboard_view = DashboardView(main_view._view_container)
    jornadas_view  = JornadasView(main_view._view_container)
    infracoes_view = InfracoesView(main_view._view_container)

    controller = DashboardController(
        service        = None,
        dashboard_view = dashboard_view,
        jornadas_view  = jornadas_view,
        infracoes_view = infracoes_view,
    )

    main_view.set_controller(controller)
    jornadas_view.set_controller(controller)
    main_view.register_views({
        "dashboard": dashboard_view,
        "jornadas":  jornadas_view,
        "infracoes": infracoes_view,
    })

    main_view.mainloop()
