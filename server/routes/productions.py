class Productions(Resource):

    @login_required
    def get(self):
        try:
            #! Pre-marshmallow code
            # serialized_prods = [
            #     prod.to_dict(
            #         only=(
            #             "id",
            #             "title",
            #             "genre",
            #             "director",
            #             "description",
            #             "budget",
            #             "image",
            #             "ongoing",
            #         )
            #     )
            #     for prod in Production.query
            # ]
            #! Marshmallow code
            serialized_prods = productions_schema.dump(Production.query)
            # resp = make_response((serialized_prods), 200, {"Content-Type": "application/json"})
            # resp.set_cookie()
            # return resp
            return serialized_prods, 200
        except Exception as e:
            return str(e), 400

    @login_required
    def post(self):
        try:
            data = (
                request.get_json()
            )  #! to jsonify data a Content-Type headers has to be set on the requester side of things
            # prod = Production(**data) #! Pre-marshmallow: model validations will kick in here
            prod = production_schema.load(
                data
            )  #! marshmallow: marshmallow first and then model validations will kick in here
            db.session.add(prod)
            db.session.commit()  #! db constraints will kick in here
            return production_schema.dump(prod), 201
        except Exception as e:
            db.session.rollback()
            return {"message": str(e)}, 422
