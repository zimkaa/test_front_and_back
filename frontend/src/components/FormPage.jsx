import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { useSearchParams } from "react-router-dom";
import { ClipLoader } from "react-spinners";

const Spinner = ({ size = 35, color = "#3498db" }) => {
  return <ClipLoader size={size} color={color} />;
};

export default function FormPage() {
  const { register, handleSubmit, setValue, formState: { errors }, setError } = useForm();

  const [searchParams, setSearchParams] = useSearchParams();
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState();

  useEffect(() => {
    const date = searchParams.get("date");
    const first_name = searchParams.get("first_name");
    const last_name = searchParams.get("last_name");
    if (date && first_name && last_name) {
      setValue("date", date);
      setValue("first_name", first_name);
      setValue("last_name", last_name);
      fetchData({ date, first_name, last_name });
    }
  }, []);

  const fetchData = async (formData) => {
    setData(null);
    setLoading(true);
    try {
      const BASE_URL = process.env.BASE_URL || 'http://localhost:8000';
      const response = await fetch(`${BASE_URL}/api/submit`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      const result = await response.json();
      if (response.status === 400) {
        Object.entries(result.error).forEach(([field, messages]) => {
          setError(field, { type: "manual", message: messages.join(", ") });
        });
        setSearchParams(formData);
      } else {
        setData(result.data);
        setSearchParams(formData);
      }
    } catch (error) {
      console.error("Error submitting form", error);
    } finally {
      setLoading(false);
    }
  };

  const onSubmit = (formData) => {
    fetchData(formData);
  };

  return (
    <div >
      {loading ? (
         <Spinner />
      ) : (
      <form onSubmit={handleSubmit(onSubmit)}>
        <input type="date" {...register("date", { required: "Date is required" })}/>
        <input type="text" {...register("first_name", { required: "First name is required" })} placeholder="First Name"/>
        <input type="text" {...register("last_name", { required: "Last name is required" })} placeholder="Last Name"/>
        <button type="submit">Submit</button>
      </form>
      )}

      {data && (
        <pre>{JSON.stringify(data, null, 2)}</pre>
      )}
      {errors.first_name && <p>{errors.first_name.message}</p>}
      {errors.last_name && <p>{errors.last_name.message}</p>}
    </div>
  );
}
