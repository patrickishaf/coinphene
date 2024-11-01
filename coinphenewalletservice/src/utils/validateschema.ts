import Joi from "joi";

export const validateSchema = async (schema: Joi.Schema<any>, data: any) => {
    const { error } = schema.validate(data, { abortEarly: false });

    if (error) {
        const message = error.details
            .map((detail: any) => detail.message.replace(/\\/g, ''))
            .join("; ");
        return message.split(";")[0].replace('"', '').replace('"', '');
    }
};