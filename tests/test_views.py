from datetime import date
from rest_framework.test import APITestCase
from teams.models import Team
from rest_framework.views import status


class TeamViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.BASE_URL = "/api/teams/"
        cls.BASE_DETAIL_URL = cls.BASE_URL + "1/"

    def test_if_a_team_can_be_created(self):
        team_data = {
            "name": "Brasil",
            "titles": 5,
            "top_scorer": "Pelé",
            "fifa_code": "BRA",
            "founded_at": "1914-06-08",
        }
        response = self.client.post(self.BASE_URL, data=team_data, format="json")

        expected_status_code = status.HTTP_201_CREATED
        result_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do POST "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, result_status_code, msg)

        expected_data = {
            "id": 1,
            "name": "Brasil",
            "titles": 5,
            "top_scorer": "Pelé",
            "fifa_code": "BRA",
            "founded_at": "1914-06-08",
        }
        result_data = response.json()
        msg = (
            "Verifique as informações da seleção retornada no POST "
            + f"em `{self.BASE_URL}` estão corretas."
        )
        self.assertEqual(expected_data, result_data, msg)

    def test_if_teams_can_be_listed(self):
        team_1_data = {
            "name": "Brasil",
            "titles": 5,
            "top_scorer": "Pelé",
            "fifa_code": "BRA",
            "founded_at": "1914-06-08",
        }
        team_2_data = {
            "name": "Argentina",
            "titles": 2,
            "top_scorer": "Lionel Messi",
            "fifa_code": "ARG",
            "founded_at": "1893-02-21",
        }

        # Criando time 1
        Team.objects.create(**team_1_data)
        # Criando time 2
        Team.objects.create(**team_2_data)

        response = self.client.get(self.BASE_URL)

        expected_status_code = status.HTTP_200_OK
        result_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do GET "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, result_status_code, msg)

        team_1_return = {**team_1_data, "id": 1}
        team_2_return = {**team_2_data, "id": 2}

        expected_data = [team_1_return, team_2_return]
        result_data = response.json()
        msg = (
            "Verifique as informações das seleções listatas no GET "
            + f"em `{self.BASE_URL}` estão corretas."
        )
        self.assertEqual(expected_data, result_data, msg)

    def test_if_a_team_can_be_updated(self):
        team_1_data = {
            "name": "Brasil",
            "titles": 5,
            "top_scorer": "Pelé",
            "fifa_code": "BRA",
            "founded_at": "1914-06-08",
        }
        # Criando time 1
        Team.objects.create(**team_1_data)

        team_1_patch_data = {
            "name": "Brasil 5000",
            "titles": 1000,
            "top_scorer": "Alejo",
            "fifa_code": "BRR",
            "founded_at": "2022-03-03",
        }
        response = self.client.patch(
            self.BASE_DETAIL_URL, data=team_1_patch_data, format="json"
        )

        expected_status_code = status.HTTP_200_OK
        result_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do PATCH "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, result_status_code, msg)

        expected_data = {**team_1_patch_data, "id": 1}
        result_data = response.json()
        msg = "Verifique se as informações das seleções são atualizadas corretamente"
        self.assertEqual(expected_data, result_data, msg)

        team = Team.objects.get(id=1)
        for key, value in expected_data.items():
            obj_value = getattr(team, key)
            if isinstance(obj_value, date):
                obj_value = obj_value.strftime("%Y-%m-%d")
            msg = f"Verifique se as alterações no campo `{key}` foram persistidas no banco"
            self.assertEqual(value, obj_value, msg)

    def test_if_a_team_can_be_deleted(self):
        team_1_data = {
            "name": "Brasil",
            "titles": 5,
            "top_scorer": "Pelé",
            "fifa_code": "BRA",
            "founded_at": "1914-06-08",
        }
        # Criando time 1
        Team.objects.create(**team_1_data)

        response = self.client.delete(self.BASE_DETAIL_URL)

        expected_status_code = status.HTTP_204_NO_CONTENT
        result_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do DELETE "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, result_status_code, msg)

        msg = "Verifique se a deleção não está retornando nenhum body"
        self.assertRaises(TypeError, response.json)

        msg = "Verifique se o registro está sendo deletado do banco corretamente"
        self.assertFalse(Team.objects.exists(), msg)

    def test_if_non_existing_id_deletion(self):
        non_existing_id_url = self.BASE_URL + "12234/"
        response = self.client.delete(non_existing_id_url)

        expected_status_code = status.HTTP_404_NOT_FOUND
        result_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do DELETE com id inválido"
            + f"em `{non_existing_id_url}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, result_status_code, msg)

        expected = {"message": "Team not found"}
        result = response.json()
        msg = "Verifique se a mensagem de DELETE com id inválido está correta"
        self.assertDictEqual(expected, result, msg)

    def test_if_non_existing_id_update(self):
        non_existing_id_url = self.BASE_URL + "12234/"
        response = self.client.patch(non_existing_id_url)

        expected_status_code = status.HTTP_404_NOT_FOUND
        result_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do PATCH com id inválido"
            + f"em `{non_existing_id_url}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, result_status_code, msg)

        expected = {"message": "Team not found"}
        result = response.json()
        msg = "Verifique se a mensagem de PATCH com id inválido está correta"
        self.assertDictEqual(expected, result, msg)

    def test_if_non_existing_id_retrieve(self):
        non_existing_id_url = self.BASE_URL + "12234/"
        response = self.client.get(non_existing_id_url)

        expected_status_code = status.HTTP_404_NOT_FOUND
        result_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do GET com id inválido"
            + f"em `{non_existing_id_url}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, result_status_code, msg)

        expected = {"message": "Team not found"}
        result = response.json()
        msg = "Verifique se a mensagem de GET com id inválido está correta"
        self.assertDictEqual(expected, result, msg)
