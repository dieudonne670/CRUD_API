from app.main import app


def test_user_delete_route_is_registered():
    delete_routes = [
        route for route in app.routes
        if getattr(route, "methods", None) and "DELETE" in route.methods
    ]

    assert any(
        getattr(route, "path", None) == "/users/{id}"
        for route in delete_routes
    )
