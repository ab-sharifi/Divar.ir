using System.ComponentModel.DataAnnotations;

namespace Divar.Data.Models
{
    public class Cities
    {
        [Key]
        public int Id { get; set; }
        public int StateId { get; set; }

        [Display(Name = "نام شهر")]
        public string CityName { get; set; }

        public virtual IEnumerable<Users> Users { get; set; }
        public virtual States States { get; set; }
    }
}
